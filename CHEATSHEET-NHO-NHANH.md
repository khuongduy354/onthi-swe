# Cheat sheet nhớ nhanh — 22 câu Kiến trúc phần mềm

Mục tiêu của file này: nhớ được **core**, tự viết/vẽ lại trong 10 phút. Chi tiết và lệnh chạy nằm trong [file 22 câu](22-CAU-HOI-VA-DAP-AN.md) và [bộ bản in](BAN-IN-NOP-KEM-22-CAU.md).

## 1. Chỉ 8 câu hỏi quality attributes

Các câu có hỏi đặc tính chất lượng: **1, 6, 8, 9, 11, 13, 17, 21**.

Không ép mỗi kiến trúc phải có cùng số lượng. Chỉ giữ các quality **nổi bật hoặc gắn trực tiếp với trade-off của kiến trúc đó**.

Công thức trả lời mỗi đặc tính:

> **Tên quality → công cụ → các bước kiểm tra → metric/kết quả mong đợi**

Bốn bước dùng lại cho mọi quality:

1. **Chuẩn bị:** chọn input/workload và ghi baseline hoặc kết quả mong đợi.
2. **Thực hiện:** chạy test hoặc tạo tình huống cần kiểm tra.
3. **Quan sát:** thu metric, log, trace hoặc output.
4. **Kết luận:** so với baseline/ngưỡng/kết quả đúng.

### Câu 1 — Microservices: nhớ **Scale – Sống – Deploy**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Scalability | Load test + Kubernetes | Chạy tải với 1 replica → tăng replica → chạy lại cùng tải → throughput tăng/latency không xấu đi |
| Availability | `kubectl delete pod` | Gửi request liên tục → xóa một pod → đo request lỗi/thời gian hồi phục → hệ thống vẫn phục vụ |
| Deployability | Docker/Kubernetes | Ghi version hiện tại → deploy riêng một service → kiểm tra service khác → chúng không phải deploy lại |

Performance vẫn cần quan sát khi test, nhưng không phải lợi ích tự động của Microservices vì network call có thể làm latency tăng.

### Câu 6 — Micro-Frontends: nhớ **Tự đổi – Tự deploy – Cô lập**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Modifiability/team autonomy | Git + CI | Sửa feature trong một MFE → xem file/repo/build bị ảnh hưởng → chỉ MFE đó cần thay đổi |
| Deployability | CI/CD | Sửa một MFE → build/deploy riêng → mở hệ thống → MFE khác không build/deploy lại |
| Fault isolation | Playwright/DevTools | Mở hệ thống → chặn/tắt một remote → reload → Shell và MFE khác vẫn dùng được |

Performance và UI consistency là trade-off cần kiểm soát, nhưng điểm phân biệt nhất của MFE là các phần có thể đổi/deploy độc lập.

### Câu 8 — JAMstack: nhớ **Nhanh – Scale – An toàn – Dễ deploy**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Performance | Lighthouse | Build/deploy trang → chạy Lighthouse → lấy LCP/TTFB → so với ngưỡng |
| Scalability/availability | CDN + load test | Chọn URL tĩnh → tăng số request → đo p95/error rate → CDN vẫn trả nhanh, ít lỗi |
| Security | OWASP ZAP/secret scanner | Build bundle → scan bundle/site → xem cảnh báo → không có secret/lỗi nghiêm trọng |
| Deployability | GitHub Actions/Netlify | Commit thay đổi → pipeline build/deploy → đo thời gian → kiểm tra trang mới và rollback |

### Câu 9 — RAG: nhớ **Tìm đúng – Nói có căn cứ – Kiến thức mới**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Retrieval relevance | Bộ câu hỏi chuẩn | Chuẩn bị câu hỏi + chunk đúng → retrieve top-k → kiểm tra chunk đúng → tính Recall@k |
| Groundedness/correctness | Đáp án/citation chuẩn | Hỏi bộ câu chuẩn → lưu answer/citation → đối chiếu tài liệu → câu trả lời được context hỗ trợ |
| Freshness | Indexer log + Vector DB | Thêm tài liệu mới → chạy indexing → hỏi nội dung mới → đo thời gian đến khi tìm được |

Latency và security vẫn phải kiểm soát, nhưng ba dòng trên là phần đặc trưng nhất của RAG.

### Câu 11 — LLM Agent: nhớ **Làm đúng – An toàn – Biết dừng – Chịu lỗi**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Correctness | Bộ task chuẩn | Chuẩn bị task + kết quả đúng → chạy agent → kiểm tra output/tool calls → tính task success rate |
| Safety | Permission/policy test | Giao task gọi tool nhạy cảm → quan sát permission check → bị chặn hoặc xin approval |
| Bounded execution | `max_steps`, timeout | Tạo task không thể hoàn thành → chạy agent → đếm bước/thời gian → dừng đúng giới hạn |
| Reliability | Mock tool lỗi | Cho tool trả timeout/5xx → chạy agent → xem retry/log → phục hồi và không lặp side effect |

### Câu 13 — Event Sourcing: nhớ **Audit – Replay – Tạo view mới**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Auditability | Event Store UI/SQL | Thực hiện vài command → mở event stream → đối chiếu từng thay đổi → đủ event, event cũ không bị sửa |
| Recoverability | Rebuild script | Ghi baseline read model → xóa/tạo bảng mới → replay events → state/count bằng baseline |
| Extensibility | Projector test | Viết projector/read model mới → replay event cũ → tạo view mới mà không sửa event cũ |

Consistency và projection lag vẫn quan trọng, nhưng audit/replay/new projection là lý do đặc trưng để chọn Event Sourcing.

### Câu 17 — Event-Driven: nhớ **Ít dính – Scale – Chịu lỗi**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Modifiability/loose coupling | Contract test | Giữ nguyên producer → thêm consumer mới theo event contract → publish event → cả hai consumer hoạt động |
| Scalability | Kafka + load test | Chạy với 1 consumer → đo throughput/lag → tăng partition/consumer → chạy lại cùng tải → so kết quả |
| Reliability | Retry/DLQ | Làm consumer lỗi tạm thời/lâu dài → publish event → xem retry → lỗi tạm phục hồi, lỗi lâu vào DLQ |

Idempotency là tactic bắt buộc để đạt reliability/correctness khi broker giao event lại.

### Câu 21 — Kappa: nhớ **Gần real-time – Scale – Hồi phục – Đúng**

| Quality | Công cụ | Các bước kiểm tra cụ thể |
|---|---|---|
| Near real-time | Kafka/Flink metrics | Ghi thời điểm event → gửi event → chờ report đổi → tính event-to-report latency và lag |
| Scalability | Partition/parallelism | Chạy tải và ghi events/giây → tăng partition/parallelism → chạy lại cùng tải → throughput tăng/lag giảm |
| Fault tolerance/replay | Checkpoint + consumer group mới | Ghi kết quả chuẩn → restart/replay vào DB mới → so count/sum → không mất/trùng |
| Correctness | Tập event chuẩn | Chuẩn bị event kể cả duplicate/out-of-order → chạy pipeline → query aggregate → đúng kết quả tính tay |

---

## 2. Nhìn từ khóa để biết phải vẽ gì

| Góc nhìn | Phải thể hiện |
|---|---|
| Logic view | Thành phần nào, làm chức năng gì, liên hệ thành phần nào, dùng công nghệ gì |
| Deployment view | Chạy trên node/container/pod nào, artifact nào, nối qua giao thức gì |
| Process view | Input cụ thể → process runtime biến đổi gì → output cụ thể; IPC/giao thức |
| Security view | Ai được vào, xác thực/phân quyền/mã hóa ở đâu |
| Scalability view | Load balancer/service → nhiều replica; thành phần nào được scale |
| Observability view | Service/producer/consumer → logs/traces/metrics → công cụ hiển thị |
| Development view | Cây thư mục; mỗi thư mục chứa gì; thay đổi một phần thế nào |
| Storage view | Service/process nào đọc hoặc ghi thực thể dữ liệu nào |

Đừng vẽ process view thành sequence diagram giữa người dùng và màn hình. Hãy vẽ **các process đang chạy**, input, phép biến đổi và output.

---

## 3. Core của từng topic và 22 câu

## Topic 1 — Microservices, câu 1–5

### Một câu định nghĩa

Microservices chia hệ thống thành các service nhỏ theo nghiệp vụ; mỗi service có thể phát triển, deploy và scale độc lập nhưng phải giao tiếp qua mạng.

```text
Client → Frontend → Search/User/Reservation → Geo/Rate
                HTTP/gRPC + service discovery
```

- **WHY:** deploy/scale/cô lập lỗi theo service.
- **Đổi lại:** lỗi mạng, dữ liệu phân tán và debug khó hơn monolith.
- **WHEN:** hệ thống lớn, nhiều nghiệp vụ/nhóm; không cần cho ứng dụng nhỏ.

| Câu | Core phải nhớ |
|---:|---|
| 1 | Quality nổi bật + deployment view + các bước deploy |
| 2 | Logic view + gRPC giữa services + process đặt phòng có input/output |
| 3 | Security: TLS/auth; Scaling: service/load balancer → nhiều replica |
| 4 | Log = việc xảy ra trong một service; Trace = đường đi toàn request qua nhiều service |
| 5 | Development tree + thay đổi một service ít ảnh hưởng phần khác + mỗi service sở hữu storage |

## Topic 2 — Micro-Frontends và JAMstack, câu 6–8

### Micro-Frontends

Chia frontend thành các UI nhỏ, được App Shell ghép lại; mỗi MFE có thể deploy riêng.

```text
Browser → App Shell → Account MFE | Search MFE | Report MFE → API
```

- Ghép bằng Module Federation/route/layout.
- Giao tiếp bằng props, URL/router hoặc event bus.
- Dùng khi frontend lớn, nhiều nhóm phát hành độc lập.

| Câu | Core phải nhớ |
|---:|---|
| 6 | Quality nổi bật + logic view + cách ghép + cách giao tiếp |
| 7 | Mỗi MFE build/deploy lên CDN riêng; Shell tải `remoteEntry.js` |

### JAMstack

JAM = **JavaScript + API + Markup**. Markup được tạo sẵn lúc build và phát qua CDN; JavaScript gọi API cho dữ liệu động.

```text
Git/CMS → Build → HTML/CSS/JS → CDN → Browser → API
```

| Câu | Core phải nhớ |
|---:|---|
| 8 | Quality nổi bật + logic view; nhanh vì trang tĩnh nằm trên CDN |

## Topic 3 — RAG và LLM Agent, câu 9–12

### RAG

RAG tìm các đoạn tài liệu liên quan rồi đưa chúng vào prompt để LLM trả lời có căn cứ.

```text
Documents → Chunk → Embedding → Vector DB
Question → Retrieve top-k → Prompt + context → LLM → Answer + citation
```

- Dùng khi cần trả lời theo tài liệu riêng/cập nhật.
- RAG **không huấn luyện lại** LLM.

| Câu | Core phải nhớ |
|---:|---|
| 9 | Quality nổi bật + logic view của indexing và query |
| 10 | Deployment: Web/API/Worker/Vector DB/LLM; index trước rồi query thử |

### LLM Agent

Agent dùng LLM để chọn và gọi tool nhiều bước cho đến khi hoàn thành hoặc chạm giới hạn.

```text
User → Agent → LLM → Permission check → Tool → Result → Agent → Answer
```

- Agent khác chatbot ở chỗ **có quyết định và gọi tool**.
- Phải có quyền, `max_steps`, timeout và checkpoint.

| Câu | Core phải nhớ |
|---:|---|
| 11 | Quality nổi bật + logic view của vòng lặp Agent–LLM–Tool |
| 12 | Deployment: API → Queue → Worker → LLM/Tools; DB lưu checkpoint |

## Topic 4 — Event Sourcing, câu 13–16

### Một câu định nghĩa

Event Sourcing lưu chuỗi event bất biến làm nguồn sự thật; trạng thái hiện tại được tạo bằng cách áp dụng lại các event theo thứ tự.

```text
Command → Aggregate → Event Store → Projector → Read Model → Query
```

- Event Store là nguồn thật; Read Model có thể xóa và rebuild.
- Eventual consistency: event đã ghi nhưng projection có thể cập nhật trễ.

| Câu | Core phải nhớ |
|---:|---|
| 13 | Quality nổi bật + logic view |
| 14 | Deploy Command API, Event Store, Projector, Read DB, Query API |
| 15 | Process xuất danh sách: Query API đọc Read Model, không replay mỗi request |
| 16 | Storage + `state rỗng → đọc event đúng thứ tự → apply → state hiện tại`; rebuild projection |

Ví dụ replay dễ nhớ:

```text
0 → Deposited(100) → 100 → Withdrawn(30) → 70
```

## Topic 5 — Event-Driven, câu 17–20

### Một câu định nghĩa

Producer phát event vào broker; consumer nhận và xử lý bất đồng bộ. Producer không cần biết consumer cụ thể.

```text
Producer → Kafka/RabbitMQ → Consumer A | Consumer B → Database
                              lỗi → Retry → DLQ
```

- Event là sự thật đã xảy ra, ví dụ `ReservationCreated`.
- Phải nhớ: eventual consistency, duplicate, retry, DLQ và idempotency.

| Câu | Core phải nhớ |
|---:|---|
| 17 | Quality nổi bật + logic view Producer–Broker–Consumers |
| 18 | Mỗi producer/broker/consumer chạy container riêng; deploy broker/topic trước |
| 19 | Input → validate schema/auth/business rule → DB + Outbox cùng transaction → publish event |
| 20 | Cùng `eventId/traceId` đi từ producer qua broker đến consumer; log + trace + metrics |

Phân biệt ba thứ ở câu 20:

- **Log:** chuyện gì đã xảy ra, ví dụ `event_published`.
- **Trace:** event/request đã đi qua thành phần nào.
- **Metric:** số tổng hợp, ví dụ throughput, error rate, consumer lag.

## Topic 6 — Kappa, câu 21–22

### Một câu định nghĩa

Kappa dùng **một stream pipeline** cho dữ liệu mới và dữ liệu tính lại; khi đổi logic thì replay event log.

```text
Data Source → Kafka log → Flink/Kafka Streams → Serving DB → Report API → Dashboard
```

- Khác Lambda: Kappa không có hai code path batch và speed.
- Kafka giữ event; stream processor validate/deduplicate/aggregate; Serving DB giữ kết quả để đọc nhanh.

| Câu | Core phải nhớ |
|---:|---|
| 21 | Quality nổi bật + logic view ở trên |
| 22 | Process: raw events → validate/deduplicate/aggregate → Serving DB → API → report |

---

## 4. Bản in đủ 22 câu

| Câu | Phải lấy bản in nào? |
|---:|---|
| 1 | Giao diện/câu lệnh kiểm tra quality + câu lệnh triển khai Microservices. **Không bắt buộc in kết quả load test.** |
| 2 | Câu lệnh cài đặt mã nguồn Microservices |
| 3 | Câu lệnh thiết lập và thực hiện scaling |
| 4 | Câu lệnh xem log/trace + ảnh giao diện kết quả Jaeger |
| 5 | Câu lệnh cài đặt thêm một component/service |
| 6 | Ảnh từng Micro-Frontend + ảnh giao diện tổng hợp |
| 7 | Câu lệnh triển khai Micro-Frontends |
| 8 | Ảnh giao diện JAMstack + cây thư mục source |
| 9 | Ảnh giao diện RAG + cây thư mục source |
| 10 | Câu lệnh **hoặc** giao diện công cụ trực tuyến dùng để triển khai RAG |
| 11 | Ảnh giao diện LLM Agent + cây thư mục source |
| 12 | Câu lệnh **hoặc** giao diện công cụ trực tuyến dùng để triển khai Agent |
| 13 | Ảnh giao diện nhập dữ liệu Event Sourcing + cây thư mục source |
| 14 | Câu lệnh **hoặc** giao diện công cụ trực tuyến dùng để triển khai Event Sourcing |
| 15 | Ảnh giao diện danh sách của Event Sourcing |
| 16 | Đề không nêu yêu cầu bản in riêng |
| 17 | Ảnh giao diện nhập dữ liệu Event-Driven + cây thư mục source |
| 18 | Câu lệnh **hoặc** giao diện công cụ trực tuyến dùng để triển khai Event-Driven |
| 19 | Đề không nêu yêu cầu bản in riêng |
| 20 | Câu lệnh xem kết quả giám sát + ảnh log/trace/monitoring |
| 21 | Ảnh giao diện nhập dữ liệu Kappa + cây thư mục source |
| 22 | Ảnh giao diện báo cáo + ảnh giao diện dữ liệu thô của báo cáo |

Nhớ bốn cụm:

- **Chỉ lệnh:** 1, 2, 3, 5, 7, 10, 12, 14, 18.
- **UI + source tree:** 8, 9, 11, 13, 17, 21.
- **UI đặc biệt:** 6, 15, 22.
- **Kết quả observability thật:** 4, 20.
- **Không nêu bản in riêng:** 16, 19.

---

## 5. Khung viết A4 trong 10 phút

1. Viết **định nghĩa một câu**.
2. Nếu hỏi quality: mỗi quality viết đủ **tool → các bước test → metric/kết quả mong đợi**.
3. Vẽ sơ đồ lớn, khoảng 5–7 box; ghi công nghệ và giao thức ngay trên box/mũi tên.
4. Viết các bước theo số `1 → 2 → 3 → 4`.
5. Kết thúc bằng 1 lợi ích và 1 trade-off.

Nếu bí, luôn quay về:

> **Input là gì? Process/component làm gì? Output là gì? Dùng công nghệ nào? Đo bằng metric nào?**
