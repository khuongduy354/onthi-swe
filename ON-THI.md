# Đáp án cốt lõi cho 22 câu Kiến trúc phần mềm

- Nội dung dưới đây chỉ giữ **core** và các ý vừa đủ để trả lời đúng câu hỏi.
- Công cụ minh họa: React, FastAPI, PostgreSQL, Kafka, Docker/Kubernetes và OpenTelemetry.
- Khi thi, thay bằng đúng công cụ và kết quả của bài thực hành nhóm mình.

## Nhớ chung cho mọi câu

- **Logic view:** các thành phần phần mềm và trách nhiệm.
- **Deployment view:** thành phần chạy ở đâu và bằng công cụ nào.
- **Process view:** input → xử lý → output.
- **Quality:** mỗi đặc tính phải đi cùng công cụ và cách đo.

---

## Câu 1 — Microservices: chất lượng và triển khai

- **Core:** chia hệ thống thành các service độc lập để có thể deploy và scale riêng.
- **1. Performance — Công cụ:** Locust/JMeter; **cách đo:** p95 latency, request/giây và error rate.
- **2. Scalability — Công cụ:** Locust + `kubectl scale`; **cách đo:** so kết quả cùng một tải trước và sau khi tăng replica.
- **3. Availability — Công cụ:** `kubectl delete pod`; **cách đo:** số request lỗi và thời gian phục hồi khi một pod chết.
- **4. Deployability — Công cụ:** GitHub Actions/Kubernetes; **cách đo:** deploy một service mà service khác không phải deploy lại.
- **5. Security — Công cụ:** Postman/OWASP ZAP; **cách đo:** không token `401`, sai quyền `403`, đúng quyền `2xx`, không có lỗi nghiêm trọng.
- **Deployment view:** `Browser → Nginx/Gateway → các service containers → database`; `service → Kafka → worker`.
- **Công cụ triển khai:** Docker đóng gói; Kubernetes chạy/scale; PostgreSQL lưu dữ liệu; Kafka truyền event.
- **Các bước:** test → build image → push registry → cấu hình DB/secret → deploy → kiểm tra health/log.
- **Bản in:** kết quả load test, trạng thái container/pod và lệnh deploy.

---

## Câu 2 — Microservices: logic, giao tiếp và tiến trình

- **Core:** logic view cho biết service nào làm gì; process view cho biết một use case chạy theo thứ tự nào.
- **Logic view:** `Web → Gateway → [Auth Service | Document Service | Search Service]`; `Document Service → Kafka → Index Worker`.
- **Công cụ:** React cho Web; FastAPI cho service; Kafka cho message; PostgreSQL/Pinecone cho dữ liệu.
- **Giao tiếp:** REST/gRPC khi cần kết quả ngay; Kafka khi xử lý nền; không đọc trực tiếp DB của service khác.
- **Process upload:** `File + token → Gateway → Document Service → lưu metadata → phát event → Worker xử lý → lưu kết quả`.
- **Output:** API trả `document_id`; cuối cùng tài liệu có trạng thái `indexed`.
- **Bản in:** cây source, lệnh cài/build và request/response.

---

## Câu 3 — Microservices: bảo mật và mở rộng

- **Core bảo mật:** chỉ đúng người và đúng quyền mới truy cập được tài nguyên.
- **Security view:** `User --HTTPS/JWT→ Gateway → Services → Database`; Secret Manager và Audit Log hỗ trợ hệ thống.
- **Công cụ:** Nginx/Kong cho TLS; Keycloak/Auth0 cho JWT; middleware kiểm quyền; Kubernetes Secret giữ khóa.
- **Core mở rộng:** Load Balancer chia request cho nhiều replica; Kafka chia event theo partition cho nhiều worker.
- **Scalability view:** `Load Balancer → [API pod 1 | pod 2 | pod N]`; `Kafka partitions → worker group`.
- **Công cụ/cách làm:** Locust tạo tải; Prometheus tìm điểm nghẽn; HPA/`kubectl scale` tăng replica; chạy lại cùng tải để so latency/throughput.
- **Bản in:** cấu hình đã che secret, lệnh HPA/scale và số pod trước-sau.

---

## Câu 4 — Microservices: logging và tracing

- **Core:** log mô tả việc xảy ra trong một service; trace nối toàn bộ đường đi của một request.
- **View:** `Gateway → Service A → Service B → OpenTelemetry Collector → [Loki | Jaeger | Prometheus] → Grafana`.
- **Công cụ:** OpenTelemetry tạo/gửi dữ liệu; Loki lưu log; Jaeger lưu trace; Prometheus/Grafana hiển thị metric.
- **Cách làm:** tạo `trace_id` → truyền qua các service → log kèm `trace_id` → gửi về Collector → tìm log và trace trên dashboard.
- **Không log:** password, token và dữ liệu nhạy cảm.
- **Bản in:** lệnh xem log, log có `trace_id`, giao diện Jaeger/Grafana.

---

## Câu 5 — Microservices: phát triển và lưu trữ

- **Core:** tách source và dữ liệu theo service để thay đổi một phần ít ảnh hưởng phần khác.
- **Development view:** `services/auth/`, `services/document/`, `services/search/`, `services/worker/`, `tests/`, `deploy/`; mỗi thư mục chứa đúng service/test/cấu hình tương ứng.
- **Ví dụ mở rộng:** thêm Notification Service nhận event `DocumentIndexed`.
- **Các bước:** định nghĩa event → tạo service mới → unit test → integration test Kafka → E2E → build/deploy riêng.
- **Storage view:** `User 1—N Document 1—N Chunk`; PostgreSQL lưu metadata; Pinecone lưu vector; Outbox lưu event chờ gửi.
- **Mục đích:** User là chủ sở hữu; Document là tài liệu; Chunk là đoạn; Vector dùng tìm kiếm; Outbox tránh mất event.
- **Bản in:** cây thư mục, sơ đồ dữ liệu và lệnh build/test service mới.

---

## Câu 6 — Micro-Frontends: chất lượng, logic, kết hợp và giao tiếp

- **Core:** App Shell ghép các giao diện nhỏ có thể phát triển và deploy độc lập.
- **Deployability — Công cụ:** CI/CD; **cách đo:** deploy một MFE mà MFE khác không build lại.
- **Fault isolation — Công cụ:** Playwright/DevTools; **cách đo:** tắt một remote, Shell và phần khác vẫn chạy.
- **Performance — Công cụ:** Lighthouse; **cách đo:** LCP, INP và kích thước JavaScript.
- **Consistency — Công cụ:** Storybook visual test; **cách đo:** giao diện không lệch thiết kế chuẩn.
- **Testability — Công cụ:** Vitest/Playwright; **cách đo:** component test và E2E pass.
- **Logic view:** `Browser → App Shell → [Account MFE | Search MFE | Report MFE] → Backend API`.
- **Kết hợp:** Shell tải MFE bằng Module Federation và đặt vào route/layout.
- **Giao tiếp:** props/callback, URL/router hoặc event bus; tránh dùng chung global state lớn.
- **Bản in:** từng MFE và giao diện tổng hợp.

---

## Câu 7 — Micro-Frontends: triển khai

- **Core:** mỗi MFE được build/deploy riêng; browser tải chúng vào App Shell.
- **Deployment view:** `Repo MFE → CI build → CDN`; `Browser → Shell → remoteEntry.js → Backend API`.
- **Công cụ:** GitHub Actions, npm/Vite/Webpack, Module Federation và Netlify/Vercel/CDN.
- **Các bước:** test/build từng MFE → upload artifact có version → cập nhật manifest của Shell → E2E → phát hành → rollback manifest nếu lỗi.
- **Bản in:** lệnh build/upload, CI log và giao diện sau deploy.

---

## Câu 8 — JAMstack: chất lượng và logic

- **Core:** tạo sẵn Markup lúc build, phát từ CDN; JavaScript tạo tương tác và gọi API cho dữ liệu động.
- **Performance — Công cụ:** Lighthouse; **cách đo:** LCP và TTFB.
- **Scalability — Công cụ:** k6/Locust; **cách đo:** request/giây, p95 và error rate của URL CDN.
- **Availability — Công cụ:** Playwright/curl; **cách đo:** tắt API, trang tĩnh vẫn trả `200` và có fallback.
- **Security — Công cụ:** OWASP ZAP/secret scanner; **cách đo:** không có lỗi nghiêm trọng hoặc secret trong bundle.
- **Deployability — Công cụ:** GitHub Actions/Netlify; **cách đo:** thời gian từ commit đến trang mới và khả năng rollback.
- **Logic view:** `Git/CMS → Next.js/Astro build → HTML/CSS/JS → CDN → Browser → API`.
- **Bản in:** giao diện, cây source và kết quả build.

---

## Câu 9 — RAG: chất lượng và logic

- **Core:** tìm đoạn tài liệu liên quan rồi đưa vào prompt để LLM trả lời có căn cứ.
- **Retrieval relevance — Công cụ:** bộ câu hỏi chuẩn/script eval; **cách đo:** Recall@k hoặc tỷ lệ top-k chứa đoạn đúng.
- **Answer/citation correctness — Công cụ:** đáp án chuẩn/kiểm tra tay; **cách đo:** tỷ lệ câu đúng và citation thật sự hỗ trợ câu trả lời.
- **Performance — Công cụ:** Locust/OpenTelemetry; **cách đo:** p95 retrieval và end-to-end latency.
- **Freshness — Công cụ:** worker log/vector DB UI; **cách đo:** thời gian từ khi thêm tài liệu đến khi tìm được.
- **Security — Công cụ:** test bằng hai tài khoản; **cách đo:** user A không lấy được chunk của user B.
- **Logic view:** `Documents → Chunk → Embedding → Vector DB`; `Question → Retrieve top-k → Prompt → LLM → Answer + citation`.
- **Công cụ cài đặt:** Python/LangChain, embedding/LLM API, Pinecone/FAISS, FastAPI và React.
- **Bản in:** giao diện hỏi đáp, citation/top-k và cây source.

---

## Câu 10 — RAG: triển khai

- **Core:** tách indexing chạy nền khỏi query phục vụ người dùng.
- **Deployment view:** `Browser → Web → Query API → [Vector DB | Embedding API | LLM API]`; `Documents → Worker → Vector DB`.
- **Công cụ:** Docker/Kubernetes, Kafka/queue, Pinecone, LLM API và Kubernetes Secret.
- **Các bước:** tạo vector index → cấu hình secret → build/deploy worker → index dữ liệu mẫu → deploy Query API/Web → hỏi thử và kiểm tra citation/log.
- **Bản in:** lệnh deploy, trạng thái container/pod, vector DB UI và giao diện query.

---

## Câu 11 — LLM-based Agent: chất lượng và logic

- **Core:** agent dùng LLM để chọn và gọi tool nhiều bước cho đến khi hoàn thành hoặc phải dừng.
- **Correctness — Công cụ:** bộ task chuẩn; **cách đo:** task success rate.
- **Safety — Công cụ:** policy test; **cách đo:** tool thiếu quyền bị chặn hoặc yêu cầu approval.
- **Bounded execution — Công cụ:** cấu hình agent; **cách đo:** dừng đúng `max_steps`, timeout hoặc cost limit.
- **Reliability — Công cụ:** mock tool; **cách đo:** tool timeout/5xx được retry và không lặp side effect.
- **Modifiability — Công cụ:** contract test; **cách đo:** thêm tool mới mà không sửa core loop.
- **Logic view:** `User → Agent → LLM → Permission Check → Tool → Result → Answer`; Memory/Checkpoint lưu trạng thái.
- **Công cụ cài đặt:** LangGraph/custom Python, LLM API, Pydantic tool schema, PostgreSQL/Redis và OpenTelemetry.
- **Bản in:** giao diện, cây source và một tool call.

---

## Câu 12 — LLM-based Agent: triển khai

- **Core:** Agent API nhận task; worker chạy agent và gọi LLM/tools; DB lưu checkpoint.
- **Deployment view:** `Client → Gateway/Auth → Agent API → Queue → Worker → [LLM | Tools]`; Worker → Checkpoint DB/Secrets/Logs.
- **Công cụ:** FastAPI, Docker/Kubernetes, Temporal/Kafka, PostgreSQL, Vault/Secret và OpenTelemetry.
- **Các bước:** định nghĩa tool/quyền → lưu secret → build/deploy API/worker/queue/DB → đặt max steps/timeout/retry → test staging → theo dõi rồi mở rộng.
- **Bản in:** lệnh/status deploy và trace một agent run.

---

## Câu 13 — Event Sourcing: chất lượng và logic

- **Core:** lưu chuỗi event bất biến; trạng thái hiện tại được tính lại từ chuỗi đó.
- **Auditability — Công cụ:** EventStoreDB UI/SQL; **cách đo:** mọi thay đổi có event và ứng dụng không sửa/xóa được.
- **Recoverability — Công cụ:** rebuild script; **cách đo:** replay tạo lại đúng state/count cũ.
- **Extensibility — Công cụ:** projector test; **cách đo:** tạo read model mới mà không đổi event cũ.
- **Performance — Công cụ:** Locust/Prometheus; **cách đo:** append p95, query p95 và projection lag.
- **Consistency — Công cụ:** pytest; **cách đo:** duplicate chỉ xử lý một lần, sai `expected_version` bị từ chối.
- **Logic view:** `Command API → Aggregate → Event Store → Projector → Read Model ← Query API`.
- **Công cụ cài đặt:** FastAPI, EventStoreDB/PostgreSQL và Python projector.
- **Bản in:** giao diện nhập, event rows và cây source.

---

## Câu 14 — Event Sourcing: triển khai

- **Core:** Command API ghi Event Store; Projector tạo Read Model; Query API đọc Read Model.
- **Deployment view:** `Command API container → Event Store`; `Event Store → Projector container → Read DB`; `Query API container → Read DB`.
- **Công cụ:** Docker/Kubernetes, EventStoreDB/PostgreSQL, volume/backup và OpenTelemetry.
- **Các bước:** deploy Event Store → tạo schema → deploy Command API → deploy Read DB/Projector → replay → deploy Query API → kiểm tra end-to-end.
- **Bản in:** lệnh deploy, Event Store UI và log projector.

---

## Câu 15 — Event Sourcing: tiến trình xuất danh sách

- **Core:** Query API đọc danh sách từ Read Model đã được projector tính sẵn, không replay mỗi lần xem.
- **Process view:** `Event Store → Projector → Read Model`; `User → UI → Query API → Read Model → JSON list → UI`.
- **Input:** token, filter và phân trang.
- **Xử lý:** kiểm quyền/tham số → query Read Model → tạo DTO.
- **Output:** danh sách, tổng số dòng và thông tin phân trang.
- **Bản in:** giao diện danh sách.

---

## Câu 16 — Event Sourcing: lưu trữ và tái tạo trạng thái

- **Core:** Event Store là nguồn sự thật; Read Model là dữ liệu được tạo lại từ events.
- **Storage view:** Event gồm `event_id`, `aggregate_id`, `version`, `type`, `payload`, `time`; Checkpoint lưu vị trí projector; Read Model lưu trạng thái hiện tại.
- **Công cụ/cài đặt:** EventStoreDB/PostgreSQL + migration; tạo event table/constraint → checkpoint/read tables → projector.
- **Luồng trạng thái:** `0 --Deposited(100)→ 100 --Withdrawn(30)→ 70`.
- **Tái tạo:** bắt đầu state rỗng/snapshot → đọc events đúng version → áp dụng tuần tự → nhận state cuối.
- **Rebuild Read Model:** tạo bảng mới → replay toàn bộ → so count/state → chuyển Query API sang bảng mới.
- **Công cụ tái tạo:** Event Store client, projector/rebuild script và DB viewer.

---

## Câu 17 — Event-Driven: chất lượng và logic

- **Core:** producer phát event; broker chuyển/giữ event; consumer độc lập xử lý.
- **Loose coupling — Công cụ:** Git/contract test; **cách đo:** thêm consumer mà producer không đổi.
- **Scalability — Công cụ:** Locust + Kafka/Grafana; **cách đo:** events/giây và lag trước/sau khi tăng partition/consumer.
- **Availability — Công cụ:** Docker/Kafka UI; **cách đo:** tắt consumer rồi bật lại, event tồn đọng vẫn được xử lý.
- **Reliability — Công cụ:** retry/DLQ dashboard; **cách đo:** lỗi tạm thời được retry, lỗi lâu vào DLQ.
- **Idempotency — Công cụ:** pytest/DB query; **cách đo:** cùng `event_id` hai lần nhưng kết quả chỉ đổi một lần.
- **Logic view:** `Producer API → Kafka → [Consumer A | Consumer B] → Databases`.
- **Công cụ cài đặt:** FastAPI, Kafka/RabbitMQ, Python consumer và PostgreSQL.
- **Bản in:** giao diện nhập, broker UI và cây source.

---

## Câu 18 — Event-Driven: triển khai

- **Core:** broker và mỗi producer/consumer chạy thành process/container riêng.
- **Deployment view:** `Client → Producer API → PostgreSQL/Outbox → Kafka → Consumer containers → Databases`.
- **Công cụ:** Docker/Kubernetes, PostgreSQL, Kafka/RabbitMQ và Grafana.
- **Các bước:** deploy broker/topic → deploy DB/consumers → deploy producer → gửi event test → kiểm tra kết quả/lag → scale consumer nếu cần.
- **Bản in:** lệnh deploy, broker UI và trạng thái consumers.

---

## Câu 19 — Event-Driven: tiến trình nhập dữ liệu

- **Core:** chỉ input hợp lệ mới được lưu và tạo event.
- **Process view:** `User → API → Validate → DB + Outbox → Kafka → Consumer → Result DB`.
- **Công cụ kiểm tra:** Pydantic/JSON Schema kiểm cấu trúc; JWT middleware kiểm quyền; service/DB constraint kiểm business rule.
- **Input sai:** trả `400/401/403/422`, không lưu.
- **Input đúng:** ghi business data + outbox trong một transaction → commit → trả ID → relay publish event.
- **Consumer:** kiểm schema/duplicate → xử lý → lưu kết quả → lỗi thì retry/DLQ.

---

## Câu 20 — Event-Driven: logging, tracing và monitoring

- **Core:** theo dõi một event từ producer qua broker đến consumer bằng các ID chung.
- **View:** `Producer → Kafka → Consumers → OpenTelemetry Collector → [Loki | Jaeger | Prometheus] → Grafana`.
- **Công cụ:** OpenTelemetry, Loki, Jaeger, Prometheus và Grafana.
- **Các bước:** tạo `event_id/correlation_id` → đặt vào header → log lúc publish/consume/retry/DLQ → tạo spans → thu lag/error/DLQ metrics → hiển thị và cảnh báo.
- **Kiểm tra:** phát một event, tìm toàn bộ log/trace theo correlation ID và xem dashboard lag.
- **Bản in:** lệnh xem log, trace và dashboard.

---

## Câu 21 — Kappa: chất lượng và logic

- **Core:** Kappa dùng một stream pipeline; muốn tính lại thì replay event log.
- **Near real time — Công cụ:** Kafka/Flink metrics; **cách đo:** event-to-report latency và lag.
- **Scalability — Công cụ:** Locust + Kafka/Flink; **cách đo:** events/giây trước/sau khi tăng partition/parallelism.
- **Fault tolerance — Công cụ:** checkpoint + Docker/Kubernetes; **cách đo:** restart processor mà không mất/trùng kết quả.
- **Replay/recovery — Công cụ:** consumer group mới + SQL; **cách đo:** replay vào DB mới cho count/sum đúng.
- **Correctness — Công cụ:** tập event chuẩn; **cách đo:** aggregate cuối đúng kể cả duplicate/out-of-order.
- **Logic view:** `Data source → Kafka log → Flink/Kafka Streams → Serving DB → Report API/Dashboard`.
- **Bản in:** giao diện nhập, Kafka UI, cây source và dashboard lag.

---

## Câu 22 — Kappa: tiến trình xuất báo cáo

- **Core:** stream processor tính sẵn số liệu; Report API chỉ đọc Serving DB.
- **Process view:** `Raw events → Kafka → Processor → Serving DB`; `User → Report API → Serving DB → Chart/Table`.
- **Input:** event dữ liệu; yêu cầu báo cáo gồm user và khoảng ngày.
- **Xử lý:** validate/deduplicate → tính tổng theo ngày → lưu aggregate/checkpoint → API kiểm quyền và query.
- **Output:** bảng/biểu đồ và thời điểm cập nhật cuối.
- **Khôi phục:** processor chạy lại từ checkpoint; đổi công thức thì replay vào bảng mới.
- **Bản in:** giao diện báo cáo và dữ liệu thô tương ứng.
