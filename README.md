# Ôn thi vấn đáp Kiến trúc phần mềm — đúng 22 câu

## Cách học và cách viết trên A4

Mỗi câu chỉ cần làm đúng ba việc:

1. **Vẽ sơ đồ trước**: box là thành phần, mũi tên ghi giao thức hoặc dữ liệu.
2. **Ghi từ khóa cạnh sơ đồ**: trách nhiệm, công cụ, các bước.
3. **Chỉ ghi điều mình giải thích được**: thầy sẽ hỏi dựa trên phần mình đã viết.

Khi nói, đi theo thứ tự: **đây là gì → sơ đồ gồm gì → luồng chạy thế nào → công cụ nào → vì sao làm vậy**.

> Thư mục ban đầu không có source code bài thực hành. Tài liệu dùng một stack mẫu dễ trình bày: React, FastAPI, PostgreSQL, Kafka, Pinecone, Docker/Kubernetes, OpenTelemetry/Grafana. Nếu bài nhóm dùng công nghệ khác thì đổi tên công nghệ, giữ nguyên vai trò của thành phần.

---

# 1. Microservices: đặc tính chất lượng và góc nhìn triển khai

## Vẽ

```text
Người dùng
    |
  HTTPS
    v
Load Balancer / Nginx
    |
API Gateway
  |        |         |
Auth     Document   Search       (Docker containers/Kubernetes)
  |        |          |
Postgres  Postgres   Pinecone
              |
            Kafka --> Index Worker
```

## Ghi và nói

Các đặc tính mong muốn:

- **Performance**: thời gian phản hồi thấp.
- **Scalability**: tăng replica khi số request tăng.
- **Availability**: một instance chết, instance khác vẫn phục vụ.
- **Modifiability/deployability**: sửa và deploy một service mà không deploy toàn hệ thống.
- **Security**: xác thực, phân quyền, mã hóa kết nối.

Cách kiểm tra:

1. Dùng JMeter/Locust tạo nhiều request.
2. Đo throughput, p95 latency và error rate.
3. Tắt một container để kiểm tra failover.
4. Tăng replica rồi chạy lại cùng bài test.
5. Dùng OWASP ZAP kiểm tra lỗi web cơ bản; dùng UptimeRobot/Pingdom kiểm tra availability.

Các bước triển khai:

1. Test và build từng service.
2. Tạo Docker image, push lên registry.
3. Cấu hình database, secret và network.
4. Chạy bằng Docker Compose hoặc `kubectl apply`.
5. Kiểm tra health endpoint, log và giao diện.

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8080/health
kubectl get pods,svc
```

**Bản in:** sơ đồ, kết quả JMeter/Locust, `docker compose ps` hoặc `kubectl get pods`.

---

# 2. Microservices: góc nhìn logic, giao tiếp và góc nhìn tiến trình

## Vẽ logic view

```text
Web UI --> API Gateway
              |--> Auth Service: đăng nhập, token
              |--> Document Service: quản lý tài liệu
              |--> Search Service: tìm kiếm

Document Service --DocumentUploaded event--> Kafka --> Index Service
Search Service ------------------------------> Pinecone
```

Giao tiếp giữa service:

- **REST/gRPC đồng bộ** khi cần kết quả ngay. Phải có timeout và retry.
- **Kafka/message bất đồng bộ** khi xử lý nền. Producer không cần chờ consumer.
- Mỗi service có trách nhiệm và dữ liệu riêng; không đọc trực tiếp bảng riêng của service khác.

## Vẽ process view: upload tài liệu

```text
User -> UI -> Gateway -> Document Service
                         1. kiểm tra file và quyền
                         2. lưu metadata
                         3. trả 202 + document_id
                         4. phát DocumentUploaded

Kafka -> Index Worker -> tách đoạn -> embedding -> Pinecone
UI -> Document Service -> xem trạng thái indexed
```

Input là file và token. Output ban đầu là `document_id`; output cuối là tài liệu đã tìm kiếm được.

**Bản in:** cây source, request/response API và log worker.

---

# 3. Microservices: góc nhìn bảo mật và mở rộng

## Vẽ security view

```text
[Internet]
    |
 HTTPS/TLS
    v
[WAF/API Gateway] -- kiểm tra JWT --> [Services]
                                          |
                              private network + tài khoản DB riêng
                                          |
                                  [Encrypted Database]

Secrets Manager: giữ API key/password
Audit Log: ghi hành động quan trọng
```

Ghi:

- Authentication xác định người dùng là ai.
- Authorization kiểm tra người dùng được truy cập tài nguyên nào.
- TLS mã hóa khi truyền; database mã hóa khi lưu.
- Token/API key để trong Secrets Manager, không ghi vào source hoặc log.
- Rate limit/WAF chống lạm dụng; service dùng quyền tối thiểu.

## Vẽ scalability view

```text
                  --> API replica 1 --|
Load Balancer ----> API replica 2 ----|--> Redis / Database
                  --> API replica N --|

Kafka partitions --> nhiều Index Worker trong consumer group
```

Các bước mở rộng:

1. Chạy load test lấy kết quả ban đầu.
2. Xác định service nghẽn bằng CPU, latency hoặc queue lag.
3. Tăng replica đúng service.
4. Chạy lại cùng bài test và so sánh.

```bash
kubectl scale deployment search-service --replicas=3
kubectl get pods
```

**Bản in:** cấu hình auth/secret đã che giá trị, lệnh scale, số pod trước và sau.

---

# 4. Microservices: góc nhìn giám sát logging và tracing

## Vẽ

```text
Request có trace_id
        |
Gateway -> Service A -> Service B
   |          |            |
   +----------+------------+--> OpenTelemetry Collector
                                  |--> Loki/ELK: logs
                                  |--> Jaeger: traces
                                  |--> Prometheus: metrics
                                                |
                                             Grafana
```

## Ghi và nói

- **Log**: chi tiết sự kiện/lỗi của từng service.
- **Trace**: đường đi của một request qua nhiều service.
- Mỗi request có `trace_id`; service truyền ID này qua HTTP, gRPC hoặc message header.
- Log nên có time, level, service, operation, trace_id và error; không log token/password.

Các bước:

1. Cài OpenTelemetry SDK cho các service.
2. Truyền trace context giữa các service.
3. Gửi log/span đến OpenTelemetry Collector.
4. Collector gửi dữ liệu đến Loki/ELK và Jaeger.
5. Gửi một request, tìm log theo `trace_id`, mở trace và xem service chậm/lỗi.

```bash
docker compose logs -f api search-service index-worker
kubectl logs -f deployment/search-service
```

**Bản in:** log có trace ID, giao diện Jaeger và Grafana.

---

# 5. Microservices: góc nhìn phát triển, thay đổi/kiểm thử và lưu trữ

## Vẽ development view

```text
project/
├── services/
│   ├── auth-service/       # đăng nhập và token
│   ├── document-service/   # tài liệu
│   ├── search-service/     # tìm kiếm
│   └── index-worker/       # xử lý event
├── shared-contracts/       # OpenAPI/event schema
├── tests/                  # contract và end-to-end test
└── deploy/                 # Docker Compose/Kubernetes
```

Ví dụ thêm Notification Service:

1. Định nghĩa event `DocumentIndexed`.
2. Tạo service mới subscribe event.
3. Unit test service mới.
4. Integration test với Kafka.
5. End-to-end test upload → index → notification.
6. Build và deploy riêng Notification Service.

Cách này ít ảnh hưởng mã nguồn cũ vì service mới chỉ phụ thuộc vào event contract.

## Vẽ storage view

```text
User 1---N Document 1---N Chunk
                    |
                    +--> Vector trong Pinecone

Document DB: id, owner_id, name, status
Chunk: id, document_id, position, vector_id
Outbox Event: event_id, type, payload, published
```

```bash
docker compose build notification-service
docker compose run --rm notification-service pytest
docker compose up -d notification-service
```

**Bản in:** cây thư mục, lệnh test/build service mới và dữ liệu trong DB.

---

# 6. Micro-Frontends: đặc tính chất lượng, logic view, kết hợp và giao tiếp

## Vẽ

```text
Browser
  |
App Shell: layout, routing, authentication
  |--------------|----------------|
Account MFE     Search MFE       Report MFE
  |              |                 |
  +--------------+-----------------+--> Backend API

React + Module Federation
```

## Ghi và nói

Đặc tính mong muốn:

- Dễ thay đổi và deploy từng giao diện độc lập.
- Một MFE lỗi, shell và MFE khác vẫn chạy.
- Tải trang nhanh, bundle không quá lớn.
- Giao diện thống nhất nhờ shared design system.
- Dễ test riêng bằng Storybook/component test.

Kiểm tra: Lighthouse đo tốc độ; tắt một remote để xem fallback; build/deploy một MFE; chạy Storybook và E2E.

Cách kết hợp: App Shell tải các remote component lúc runtime bằng Module Federation, sau đó đặt chúng vào đúng route/layout.

Cách giao tiếp:

- Shell truyền props/callback cho MFE.
- Dùng router/URL cho navigation.
- Dùng event bus cho sự kiện đơn giản.
- Tránh shared mutable global state giữa tất cả MFE.

**Bản in:** giao diện từng MFE, giao diện tổng hợp và Storybook.

---

# 7. Micro-Frontends: góc nhìn triển khai

## Vẽ

```text
Git repo Shell --> CI build --> CDN /shell
Git repo Search MFE --> CI build --> CDN /search/remoteEntry.js
Git repo Report MFE --> CI build --> CDN /report/remoteEntry.js

Browser --> tải Shell --> tải các remote từ CDN --> gọi Backend API
```

## Các bước triển khai

1. Mỗi MFE chạy lint, test và build riêng.
2. Đưa artifact có version/hash lên CDN.
3. Cập nhật manifest/import map của Shell.
4. Mở preview và chạy E2E từ Shell.
5. Deploy canary, theo dõi lỗi tải remote.
6. Nếu lỗi, trỏ manifest về version cũ.

```bash
npm ci
npm test
npm run build
npx storybook build --quiet
```

**Bản in:** lệnh build/deploy, trang hosting/CDN và giao diện sau deploy.

---

# 8. JAMstack: đặc tính chất lượng và góc nhìn logic

## Vẽ

```text
Git / Headless CMS
        |
     CI Build
        |
Next.js/Astro tạo HTML, CSS, JS tĩnh
        |
       CDN ----------------> Browser
                               |
                               +--> API cho dữ liệu động
```

## Ghi và nói

JAMstack gồm JavaScript, API và Markup được tạo trước. Trang tĩnh được phát từ CDN.

Đặc tính mong muốn:

- Nhanh và chịu tải tốt vì file ở CDN.
- Availability cao vì không cần origin xử lý mỗi trang.
- Ít bề mặt tấn công hơn.
- Deploy dễ: push Git → build → publish.

Kiểm tra:

1. Dùng Lighthouse đo performance.
2. Load test URL CDN.
3. Tắt API và kiểm tra trang tĩnh vẫn mở.
4. Thay content, build lại và kiểm tra nội dung mới.

Logic: content đi vào static-site generator lúc build; browser nhận HTML từ CDN; chỉ phần động mới gọi API.

**Bản in:** giao diện, cây thư mục và kết quả `npm run build`.

---

# 9. RAG: đặc tính chất lượng và góc nhìn logic

## Vẽ

```text
INDEXING:
PDF/Notion/GitHub -> Loader -> Clean -> Chunk -> Embedding -> Pinecone

QUERY:
User question -> Query embedding -> tìm top-k trong Pinecone
              -> ghép question + context -> LLM -> Answer + citations
```

## Ghi và nói

RAG lấy tài liệu liên quan làm context cho LLM trước khi sinh câu trả lời.

Đặc tính mong muốn:

- **Độ liên quan**: top-k chunks đúng với câu hỏi.
- **Độ chính xác**: câu trả lời dựa trên context và citation đúng.
- **Performance**: thời gian query thấp.
- **Freshness**: tài liệu mới sớm tìm được.
- **Security**: user chỉ retrieve tài liệu mình được phép đọc.
- **Reliability**: indexing retry được, không ghi vector trùng.

Cách kiểm tra:

1. Chuẩn bị bộ câu hỏi và tài liệu đúng mong đợi.
2. Kiểm tra chunks top-k.
3. Kiểm tra câu trả lời và citations.
4. Đo p95 latency và error rate.
5. Thêm tài liệu mới rồi kiểm tra thời gian đến khi tìm được.
6. Thử user khác để kiểm tra tenant filter.

Công cụ mẫu: FastAPI, embedding/LLM API, Pinecone, pytest, Locust.

**Bản in:** giao diện hỏi đáp, citations, cây source và một vector record có metadata.

---

# 10. RAG: góc nhìn triển khai

## Vẽ

```text
Browser -> Web/CDN -> Query API container
                         |--> LLM API
                         |--> Embedding API
                         +--> Pinecone

Data sources -> Crawler container -> Queue/Temporal -> Index Worker -> Pinecone

Tất cả container -> OpenTelemetry/Grafana
```

## Các bước triển khai

1. Tạo Pinecone index đúng dimension của embedding model.
2. Cấu hình secret cho LLM, embedding và Pinecone.
3. Build image cho Query API, Crawler và Worker.
4. Deploy queue/workflow và worker.
5. Chạy indexing một lượng dữ liệu nhỏ và kiểm tra vector.
6. Deploy Query API và Web.
7. Hỏi một câu đã biết đáp án; kiểm tra citation, log và latency.
8. Sau khi ổn mới index toàn bộ dữ liệu.

```bash
docker compose up -d query-api crawler index-worker
docker compose logs -f index-worker
curl -X POST http://localhost:8000/query \
  -H 'Content-Type: application/json' \
  -d '{"question":"What is software architecture?"}'
```

**Bản in:** lệnh triển khai, trạng thái containers, Pinecone UI và giao diện query.

---

# 11. LLM-based Agent: đặc tính chất lượng và góc nhìn logic

## Vẽ

```text
User -> Chat UI -> Agent Orchestrator <-> LLM
                       |
                       v
                  Permission Check
                       |
             Tool Registry: GitHub, RAG, Search
                       |
                   Tool Result
                       |
                 Agent trả lời

Memory/Checkpoint và Audit Log nối với Agent Orchestrator
```

## Ghi và nói

Agent dùng LLM để chọn và gọi tool nhiều bước nhằm hoàn thành mục tiêu.

Đặc tính mong muốn:

- Hoàn thành đúng nhiệm vụ.
- Chỉ gọi tool và dữ liệu được cấp quyền.
- Có giới hạn bước, thời gian và chi phí.
- Retry/resume được khi tool lỗi.
- Có log/audit cho từng tool call.
- Dễ thêm tool mới qua interface chung.

Cách kiểm tra:

1. Tạo danh sách task có kết quả mong đợi.
2. Mock tool để test agent flow.
3. Test tool timeout/error và agent retry.
4. Test user không có quyền.
5. Đo task success, latency, token cost và số tool calls.

**Bản in:** giao diện agent, cây source và một tool call thành công/thất bại.

---

# 12. LLM-based Agent: góc nhìn triển khai

## Vẽ

```text
Client -> API Gateway/Auth -> Agent API
                              |
                        Temporal/Queue
                              |
                         Agent Workers
                         |     |      |
                       LLM   RAG   Tool Gateway
                                     |
                              GitHub/External APIs

Workers -> Checkpoint DB, Secrets Manager, Observability
```

## Các bước triển khai

1. Định nghĩa schema cho từng tool và quyền cần thiết.
2. Lưu API key/token trong Secrets Manager.
3. Build Agent API và Worker images.
4. Deploy workflow/queue, checkpoint DB và workers.
5. Cấu hình max steps, timeout, retry và cost limit.
6. Test ở staging bằng read-only hoặc mock tools.
7. Deploy cho một nhóm user nhỏ bằng feature flag.
8. Theo dõi task success, lỗi, latency và cost rồi mới mở rộng.

**Bản in:** giao diện công cụ deploy, trạng thái worker và trace một agent run.

---

# 13. Event Sourcing: đặc tính chất lượng và góc nhìn logic

## Vẽ

```text
UI --Command--> Command API --> Aggregate kiểm tra business rule
                                      |
                                      v
                           Append-only Event Store
                                      |
                                  Projector
                                      |
                                  Read Model
                                      |
UI <--Result-- Query API <-------------+
```

## Ghi và nói

Event Sourcing lưu các sự kiện đã xảy ra thay vì chỉ lưu trạng thái cuối.

Ví dụ: lưu `QuizAnswered(+10)`, `AnswerCorrected(-2)` thay vì chỉ lưu `score=8`.

Đặc tính mong muốn:

- Audit được lịch sử thay đổi.
- Có thể khôi phục trạng thái bằng replay events.
- Tạo thêm read model/report mới từ events cũ.
- Append event nhanh; query nhanh qua read model.
- Không mất hoặc ghi trùng event.

Cách kiểm tra: gửi command và xem event; xóa read model rồi replay; so trạng thái trước/sau; gửi duplicate command; tạo concurrent update để kiểm tra version.

Công cụ: EventStoreDB hoặc PostgreSQL append-only table, projector, PostgreSQL read model.

**Bản in:** giao diện nhập dữ liệu, event rows và cây source.

---

# 14. Event Sourcing: góc nhìn triển khai

## Vẽ

```text
Browser -> Command API containers -> Event Store
Browser -> Query API containers   -> Read Database
Event Store -> Subscription -> Projector Workers -> Read Database

Event Store -> Backup
Tất cả services -> Logs/Metrics
```

## Các bước triển khai

1. Deploy Event Store có volume, backup và authentication.
2. Tạo event schema gồm event ID, aggregate ID, type, version, payload, time.
3. Deploy Command API và test append event.
4. Deploy Read DB và Projector.
5. Replay events để tạo read model.
6. Deploy Query API và kiểm tra dữ liệu.
7. Theo dõi append error và projection lag.

```bash
docker compose up -d eventstore command-api projector read-db query-api
docker compose logs -f projector
```

**Bản in:** lệnh triển khai, Event Store UI và trạng thái projector.

---

# 15. Event Sourcing: process view xuất một danh sách

## Vẽ

```text
Trước đó:
Event Store -> Projector -> Read Model chứa danh sách hiện tại

Khi người dùng xem:
User -> UI -> Query API
               1. kiểm tra token, filter, page
               2. query Read Model
               3. đổi dữ liệu thành DTO
UI <- JSON list + total <- Query API
```

## Ghi và nói

Ví dụ danh sách các câu đã trả lời:

- Input: user ID trong token, page, page size và filter.
- Query API kiểm tra quyền và tham số.
- Query API đọc read model đã được projector tạo sẵn.
- Output: danh sách, tổng số phần tử và thông tin phân trang.
- Không replay toàn bộ event cho mỗi lần xem vì sẽ chậm.
- Nếu projector chưa xử lý hết event, danh sách có thể chậm cập nhật một khoảng ngắn.

**Bản in:** giao diện danh sách và dữ liệu tương ứng trong read model.

---

# 16. Event Sourcing: lưu trữ, luồng dữ liệu và tái tạo trạng thái

## Vẽ storage

```text
Event Stream
  aggregate_id
  current_version
       |
       +---N Domain Event
              event_id
              aggregate_id
              version
              event_type
              payload
              occurred_at

Projector Checkpoint: projector_name, last_position
Read Model: entity_id, current_state, source_version
```

## Vẽ luồng trạng thái

```text
score=0 --QuizAnswered(+10)--> score=10
         --QuizAnswered(+8)--> score=18
         --AnswerCorrected(-2)--> score=16
```

## Các bước tái tạo

1. Đọc events của aggregate theo đúng version.
2. Bắt đầu bằng trạng thái rỗng hoặc snapshot gần nhất.
3. Lần lượt áp dụng từng event lên state.
4. Kết quả cuối là trạng thái hiện tại.
5. Muốn rebuild toàn bộ read model: tạo bảng mới, reset checkpoint, replay tất cả events.
6. So sánh count/trạng thái; đúng rồi mới cho Query API dùng bảng mới.

Công cụ: EventStoreDB/PostgreSQL, projector script, checkpoint table và DB viewer.

**Bản in:** Event Store trước replay, Read Model sau replay và lệnh/script rebuild.

---

# 17. Event-Driven: đặc tính chất lượng và góc nhìn logic

## Vẽ

```text
Upload UI -> Document API -> Document DB
                    |
             DocumentUploaded
                    v
                  Kafka
          |-----------|------------|
       Extractor    Audit       Notification
          |
     TextExtracted
          v
        Kafka -> Index Consumer -> Pinecone
```

## Ghi và nói

Producer phát event; broker chuyển event; consumer đăng ký và xử lý. Producer không cần biết tất cả consumers.

Đặc tính mong muốn:

- Dễ thêm consumer mà không sửa producer.
- Scale consumer để xử lý nhiều event.
- Broker giữ event khi consumer tạm thời chết.
- Xử lý retry và không ghi trùng.
- Theo dõi được event từ producer đến consumer.

Cách kiểm tra:

1. Phát event test và kiểm tra tất cả consumer cần thiết.
2. Tắt consumer, phát event, bật lại và kiểm tra event vẫn được xử lý.
3. Gửi duplicate event để kiểm tra idempotency.
4. Tạo tải, đo events/second và consumer lag.
5. Thêm consumer mới và chứng minh producer không đổi.

Công cụ: Kafka/RabbitMQ, FastAPI/Node, PostgreSQL, Docker, Locust, Grafana.

**Bản in:** UI nhập dữ liệu, Kafka/topic UI và cây source.

---

# 18. Event-Driven: góc nhìn triển khai

## Vẽ

```text
Client -> API containers -> PostgreSQL
               |
          Outbox Relay
               |
        Kafka cluster/topics
          |       |       |
      Extractor Indexer Notifier     (consumer containers)
                  |
               Pinecone

Kafka/consumers -> OpenTelemetry/Grafana
```

## Các bước triển khai

1. Deploy Kafka/RabbitMQ và tạo topic/queue.
2. Cấu hình replication, retention và quyền truy cập.
3. Deploy consumers trước.
4. Deploy database/outbox relay.
5. Deploy producer API.
6. Gửi một event test và kiểm tra toàn bộ luồng.
7. Theo dõi consumer lag, retry và dead-letter queue.
8. Tăng consumer replicas nếu lag cao.

```bash
docker compose up -d kafka api extractor indexer notifier
docker compose logs -f extractor indexer
kubectl scale deployment indexer --replicas=3
```

**Bản in:** lệnh triển khai, broker UI và trạng thái consumers.

---

# 19. Event-Driven: process view nhập dữ liệu và kiểm tra hợp lệ

## Vẽ

```text
User -> API: dữ liệu + token + idempotency key
          |
          +-- kiểm tra schema/type/required fields
          +-- kiểm tra authentication/authorization
          +-- kiểm tra business rule
          |
      invalid -> trả 400/403, không lưu
          |
        valid
          v
DB transaction: lưu dữ liệu + Outbox Event
          |
        trả 202 + id
          |
Outbox Relay -> Kafka -> Consumer
                         |
                    validate event
                    xử lý và lưu kết quả
                    lỗi tạm thời -> retry
                    lỗi nhiều lần -> DLQ
```

## Ghi và nói

- Outbox bảo đảm dữ liệu và event được ghi trong cùng DB transaction.
- Consumer kiểm tra `event_id`; nếu đã xử lý thì bỏ qua để tránh duplicate.
- Chỉ ack event sau khi lưu kết quả thành công.

Các test cần nêu: input sai không tạo row/event; crash sau DB commit thì relay vẫn publish; duplicate chỉ tạo một kết quả; event lỗi nhiều lần đi vào DLQ.

**Bản in:** một request hợp lệ, một request không hợp lệ, event và dữ liệu đã lưu.

---

# 20. Event-Driven: observability logging và tracing

## Vẽ

```text
Producer --event_id/correlation_id--> Kafka --> Consumer A --> Kafka --> Consumer B
   |                                      |                         |
   +--------------------------------------+-------------------------+
                                  OpenTelemetry
                         | logs | metrics | traces |
                                  Grafana/Jaeger
```

## Các bước

1. Producer tạo `event_id`, `correlation_id` và trace context.
2. Đưa các ID vào event/message header.
3. Producer log lúc publish; consumer log lúc nhận, xử lý, retry hoặc đưa vào DLQ.
4. Consumer tạo trace span khi xử lý.
5. Thu metrics: event rate, processing time, consumer lag, retry count, DLQ size.
6. Gửi dữ liệu đến OpenTelemetry Collector, Grafana và Jaeger.
7. Chọn một correlation ID và tìm toàn bộ đường đi của event.

```bash
docker compose logs -f producer consumer-a consumer-b
```

**Bản in:** log theo correlation ID, trace trên Jaeger và dashboard consumer lag/DLQ.

---

# 21. Kappa: đặc tính chất lượng và góc nhìn logic

> Câu hỏi cho chọn Lambda hoặc Kappa. Chọn **Kappa** và chỉ trình bày Kappa.

## Vẽ

```text
Ứng dụng/Data Sources
        |
       events
        v
Kafka durable event log
        |
Flink/Stream Processor
        |
Serving Database
        |
Report API -> Dashboard

Khi đổi logic:
Kafka log --replay--> Processor v2 --> Serving DB v2
```

## Ghi và nói

Kappa dùng một stream pipeline cho cả dữ liệu mới và việc tính lại. Muốn tính lại thì replay log.

Đặc tính mong muốn:

- Report cập nhật gần real time.
- Scale bằng partitions và nhiều processor instances.
- Processor chết có thể chạy lại từ checkpoint.
- Replay log tạo lại serving data.
- Có thể chạy logic v2 song song với v1.

Cách kiểm tra:

1. Tạo event có kết quả thống kê biết trước.
2. Đo throughput, latency và consumer lag.
3. Tăng partitions/processor rồi chạy lại.
4. Tắt processor, bật lại và kiểm tra resume.
5. Replay log vào DB mới rồi so count/kết quả.

Công cụ: Kafka, Flink/Kafka Streams, PostgreSQL/ClickHouse, Prometheus/Grafana, Locust.

**Bản in:** UI nhập dữ liệu, Kafka UI, source tree và dashboard lag.

---

# 22. Kappa: process view xuất báo cáo thống kê

## Vẽ

```text
Student trả lời câu hỏi
        |
AnswerSubmitted event
        v
Kafka -> Stream Processor
             1. kiểm tra event
             2. bỏ duplicate
             3. tính total/correct theo ngày
             4. lưu kết quả + checkpoint
                        |
                  Serving Database
                        |
User -> Report UI -> Report API -> query kết quả đã tính
User <- bảng/biểu đồ + thời điểm cập nhật cuối
```

## Ghi và nói

- Input event: `event_id`, `user_id`, `correct`, `event_time`.
- Processor cập nhật `total_answers`, `correct_answers`, `accuracy` theo ngày.
- Report API nhận user, khoảng ngày và timezone; kiểm tra quyền rồi đọc dữ liệu đã tổng hợp.
- Output là bảng/biểu đồ cùng `last_processed_at` để biết độ mới.
- Duplicate event không được cộng hai lần.
- Processor chết thì resume từ checkpoint.
- Khi đổi công thức, replay Kafka log vào bảng v2, kiểm tra đúng rồi chuyển Report API sang bảng mới.

**Bản in:** giao diện báo cáo, raw events trong Kafka và rows trong serving database.

---

# Checklist trước khi thi

Với câu bốc được, kiểm tra trên A4 đã có:

- [ ] Sơ đồ đúng loại view mà đề yêu cầu.
- [ ] Tên và trách nhiệm của từng thành phần.
- [ ] Nhãn trên mũi tên: REST, gRPC, event hoặc dữ liệu.
- [ ] Công cụ đã sử dụng hoặc có thể sử dụng.
- [ ] Các bước theo đúng thứ tự.
- [ ] Input và output nếu là process view.
- [ ] Metric/cách kiểm tra nếu hỏi quality attributes.
- [ ] Danh sách bản in liên quan trực tiếp đến câu.

Chỉ viết các ý trên; không tự mở rộng sang nội dung ngoài câu hỏi.
