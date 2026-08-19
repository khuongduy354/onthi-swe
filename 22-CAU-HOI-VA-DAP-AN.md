# 22 câu hỏi và đáp án ôn thi Kiến trúc phần mềm

- **Đề gốc:** [PDF 22 câu hỏi vấn đáp](materials/22-cau-hoi-thi-kien-truc-phan-mem.pdf) — GV. TS. Ngô Huy Biên, 2026.
- Mỗi câu gồm **đề bài rút gọn** và **đáp án cốt lõi** ngay bên dưới.
- Nội dung chỉ giữ các ý vừa đủ để trả lời đúng câu hỏi.

## Kiến thức chung

- **Khái niệm:** trả lời WHAT → HOW → WHY → WHEN.
- **Logic view:** chức năng/trách nhiệm → quan hệ → công nghệ/ngôn ngữ của từng thành phần.
- **Deployment view:** node phần cứng/phần mềm → artifact/module → giao thức kết nối.
- **Process view:** input cụ thể → biến đổi → output cụ thể → công nghệ thực hiện.
- **Quality:** mỗi đặc tính đi cùng công cụ, cách kiểm tra và metric.
- **Bằng chứng:** chỉ nói điều đã thực hành; nộp đúng bản in giao diện/câu lệnh liên quan.
- **Thời gian:** 10 phút viết A4 không dùng tài liệu → 2 phút chọn bản in → 5–10 phút vấn đáp.
- **Chấm điểm:** giấy A4 trống/không liên quan là 0; trả lời thiếu hoặc thiếu bản in tối đa 8; đủ ý và đúng bản in được trên 8–10 điểm.

---

## Câu 1 — Microservices: chất lượng và triển khai

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Liệt kê công cụ có thể dùng để kiểm tra các đặc tính đó.
- Trình bày các bước kiểm tra.
- Vẽ **deployment view**.
- Ghi công cụ triển khai cho từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** giao diện/câu lệnh kiểm tra chất lượng và câu lệnh triển khai.

### Đáp án cốt lõi

- **Core:** chia hệ thống thành các service độc lập để có thể deploy và scale riêng.
- **Khi dùng:** hệ thống/đội ngũ lớn, cần phát hành hoặc scale từng chức năng độc lập; đổi lại vận hành phức tạp hơn monolith.
- **1. Performance — Công cụ:** Locust/JMeter; **cách đo:** p95 latency, request/giây và error rate.
- **2. Scalability — Công cụ:** Locust + `kubectl scale`; **cách đo:** so kết quả cùng một tải trước và sau khi tăng replica.
- **3. Availability — Công cụ:** `kubectl delete pod`; **cách đo:** số request lỗi và thời gian phục hồi khi một pod chết.
- **4. Deployability — Công cụ:** GitHub Actions/Kubernetes; **cách đo:** deploy một service mà service khác không phải deploy lại.
- **5. Security — Công cụ:** Postman/OWASP ZAP; **cách đo:** không token `401`, sai quyền `403`, đúng quyền `2xx`, không có lỗi nghiêm trọng.
- **Deployment view:** `Browser --HTTPS→ Nginx/Gateway --REST→ các service containers --SQL→ database`; `service --event→ Kafka → worker`.
- **Công cụ triển khai:** Docker đóng gói; Kubernetes chạy/scale; PostgreSQL lưu dữ liệu; Kafka truyền event.
- **Các bước:** test → build image → push registry → cấu hình DB/secret → deploy → kiểm tra health/log.
- **Bản in:** kết quả load test, trạng thái container/pod và lệnh deploy.

---

## Câu 2 — Microservices: logic, giao tiếp và tiến trình

### Đề bài rút gọn

- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách các service giao tiếp với nhau.
- Vẽ **process view** cho một use case cụ thể.
- **Nộp kèm:** câu lệnh cài đặt mã nguồn hệ thống.

### Đáp án cốt lõi

- **Core:** logic view cho biết service nào làm gì; process view cho biết một use case chạy theo thứ tự nào.
- **Logic view:** `Web → Gateway → [Auth Service | Document Service | Search Service]`; `Document Service → Kafka → Index Worker`.
- **Công cụ:** React cho Web; FastAPI cho service; Kafka cho message; PostgreSQL/Pinecone cho dữ liệu.
- **Giao tiếp:** REST/gRPC khi cần kết quả ngay; Kafka khi xử lý nền; không đọc trực tiếp DB của service khác.
- **Process upload:** `File + token → Gateway → Document Service → lưu metadata → phát event → Worker xử lý → lưu kết quả`.
- **Output:** API trả `document_id`; cuối cùng tài liệu có trạng thái `indexed`.
- **Bản in:** cây source, lệnh cài/build và request/response.

---

## Câu 3 — Microservices: bảo mật và mở rộng

### Đề bài rút gọn

- Vẽ **security view**.
- Ghi công cụ dùng để cài đặt bảo mật cho từng thành phần.
- Vẽ **scalability view**.
- Ghi công cụ dùng để mở rộng từng thành phần.
- **Nộp kèm:** câu lệnh thiết lập khả năng mở rộng và câu lệnh thực hiện scale hệ thống.

### Đáp án cốt lõi

- **Core bảo mật:** chỉ đúng người và đúng quyền mới truy cập được tài nguyên.
- **Security view:** `User --HTTPS/JWT→ Gateway → Services → Database`; Secret Manager và Audit Log hỗ trợ hệ thống.
- **Công cụ:** Nginx/Kong cho TLS; Keycloak/Auth0 cho JWT; middleware kiểm quyền; Kubernetes Secret giữ khóa.
- **Core mở rộng:** Load Balancer chia request cho nhiều replica; Kafka chia event theo partition cho nhiều worker.
- **Scalability view:** `Load Balancer → [API pod 1 | pod 2 | pod N]`; `Kafka partitions → worker group`.
- **Công cụ/cách làm:** Locust tạo tải; Prometheus tìm điểm nghẽn; HPA/`kubectl scale` tăng replica; chạy lại cùng tải để so latency/throughput.
- **Bản in:** cấu hình đã che secret, lệnh HPA/scale và số pod trước-sau.

---

## Câu 4 — Microservices: logging và tracing

### Đề bài rút gọn

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện kết quả thu được.

### Đáp án cốt lõi

- **Core:** log mô tả việc xảy ra trong một service; trace nối toàn bộ đường đi của một request.
- **View:** `Gateway → Service A → Service B → OpenTelemetry Collector → [Loki | Jaeger | Prometheus] → Grafana`.
- **Công cụ:** OpenTelemetry tạo/gửi dữ liệu; Loki lưu log; Jaeger lưu trace; Prometheus/Grafana hiển thị metric.
- **Cách làm:** tạo `trace_id` → truyền qua các service → log kèm `trace_id` → gửi về Collector → tìm log và trace trên dashboard.
- **Không log:** password, token và dữ liệu nhạy cảm.
- **Bản in:** lệnh xem log, log có `trace_id`, giao diện Jaeger/Grafana.

---

## Câu 5 — Microservices: phát triển và lưu trữ

### Đề bài rút gọn

- Vẽ **development view**.
- Ghi mục đích của từng thư mục trên sơ đồ.
- Nêu một ví dụ thay đổi hoặc mở rộng hệ thống.
- Trình bày từng bước thay đổi, mở rộng và kiểm thử sao cho ít ảnh hưởng toàn bộ mã nguồn.
- Vẽ **storage view**.
- Ghi mục đích của từng thực thể lưu trữ.
- **Nộp kèm:** câu lệnh cài đặt thêm một thành phần mới.

### Đáp án cốt lõi

- **Core:** tách source và dữ liệu theo service để thay đổi một phần ít ảnh hưởng phần khác.
- **Development view:** `services/auth/`, `services/document/`, `services/search/`, `services/worker/`, `tests/`, `deploy/`; mỗi thư mục chứa đúng service/test/cấu hình tương ứng.
- **Ví dụ mở rộng:** thêm Notification Service nhận event `DocumentIndexed`.
- **Các bước:** định nghĩa event → tạo service mới → unit test → integration test Kafka → E2E → build/deploy riêng.
- **Storage view:** `User 1—N Document 1—N Chunk`; PostgreSQL lưu metadata; Pinecone lưu vector; Outbox lưu event chờ gửi.
- **Mục đích:** User là chủ sở hữu; Document là tài liệu; Chunk là đoạn; Vector dùng tìm kiếm; Outbox tránh mất event.
- **Bản in:** cây thư mục, sơ đồ dữ liệu và lệnh build/test service mới.

---

## Câu 6 — Micro-Frontends: chất lượng, logic, kết hợp và giao tiếp

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách kết hợp các giao diện thành hệ thống hoàn chỉnh.
- Giải thích cách các giao diện giao tiếp với nhau.
- **Nộp kèm:** giao diện từng Micro-Frontend và giao diện tổng hợp.

### Đáp án cốt lõi

- **Core:** App Shell ghép các giao diện nhỏ có thể phát triển và deploy độc lập.
- **Khi dùng:** frontend lớn, nhiều nhóm cần phát hành riêng; ứng dụng nhỏ thường không cần vì tăng độ phức tạp tích hợp.
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

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh triển khai.

### Đáp án cốt lõi

- **Core:** mỗi MFE được build/deploy riêng; browser tải chúng vào App Shell.
- **Deployment view:** `Repo MFE → CI build → CDN`; `Browser --HTTPS→ Shell/CDN → remoteEntry.js --HTTPS→ Backend API`.
- **Công cụ:** GitHub Actions, npm/Vite/Webpack, Module Federation và Netlify/Vercel/CDN.
- **Các bước:** test/build từng MFE → upload artifact có version → cập nhật manifest của Shell → E2E → phát hành → rollback manifest nếu lỗi.
- **Bản in:** lệnh build/upload, CI log và giao diện sau deploy.

---

## Câu 8 — JAMstack: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** tạo sẵn Markup lúc build, phát từ CDN; JavaScript tạo tương tác và gọi API cho dữ liệu động.
- **Khi dùng:** website nhiều nội dung tĩnh, cần tải nhanh và deploy đơn giản; không phù hợp phần động thời gian thực quá phức tạp.
- **Performance — Công cụ:** Lighthouse; **cách đo:** LCP và TTFB.
- **Scalability — Công cụ:** k6/Locust; **cách đo:** request/giây, p95 và error rate của URL CDN.
- **Availability — Công cụ:** Playwright/curl; **cách đo:** tắt API, trang tĩnh vẫn trả `200` và có fallback.
- **Security — Công cụ:** OWASP ZAP/secret scanner; **cách đo:** không có lỗi nghiêm trọng hoặc secret trong bundle.
- **Deployability — Công cụ:** GitHub Actions/Netlify; **cách đo:** thời gian từ commit đến trang mới và khả năng rollback.
- **Logic view:** `Git/CMS → Next.js/Astro build → HTML/CSS/JS → CDN → Browser → API`.
- **Bản in:** giao diện, cây source và kết quả build.

---

## Câu 9 — RAG: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** tìm đoạn tài liệu liên quan rồi đưa vào prompt để LLM trả lời có căn cứ.
- **Khi dùng:** LLM cần trả lời theo tài liệu riêng hoặc thường xuyên cập nhật mà không huấn luyện lại model.
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

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án cốt lõi

- **Core:** tách indexing chạy nền khỏi query phục vụ người dùng.
- **Deployment view:** `Browser --HTTPS→ Web --REST→ Query API --HTTPS→ [Vector DB | Embedding API | LLM API]`; `Documents → Worker → Vector DB`.
- **Công cụ:** Docker/Kubernetes, Kafka/queue, Pinecone, LLM API và Kubernetes Secret.
- **Các bước:** tạo vector index → cấu hình secret → build/deploy worker → index dữ liệu mẫu → deploy Query API/Web → hỏi thử và kiểm tra citation/log.
- **Bản in:** lệnh deploy, trạng thái container/pod, vector DB UI và giao diện query.

---

## Câu 11 — LLM-based Agent: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** agent dùng LLM để chọn và gọi tool nhiều bước cho đến khi hoàn thành hoặc phải dừng.
- **Khi dùng:** nhiệm vụ cần quyết định nhiều bước hoặc gọi công cụ; chatbot chỉ trả lời văn bản thì không cần agent.
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

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án cốt lõi

- **Core:** Agent API nhận task; worker chạy agent và gọi LLM/tools; DB lưu checkpoint.
- **Deployment view:** `Client --HTTPS→ Gateway/Auth --REST→ Agent API → Queue → Worker --HTTPS→ [LLM | Tools]`; Worker → Checkpoint DB/Secrets/Logs.
- **Công cụ:** FastAPI, Docker/Kubernetes, Temporal/Kafka, PostgreSQL, Vault/Secret và OpenTelemetry.
- **Các bước:** định nghĩa tool/quyền → lưu secret → build/deploy API/worker/queue/DB → đặt max steps/timeout/retry → test staging → theo dõi rồi mở rộng.
- **Bản in:** lệnh/status deploy và trace một agent run.

---

## Câu 13 — Event Sourcing: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** lưu chuỗi event bất biến; trạng thái hiện tại được tính lại từ chuỗi đó.
- **Khi dùng:** cần audit đầy đủ, replay hoặc tạo nhiều read model; không nên dùng nếu CRUD đơn giản và không cần lịch sử.
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

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án cốt lõi

- **Core:** Command API ghi Event Store; Projector tạo Read Model; Query API đọc Read Model.
- **Deployment view:** `Command API container --append→ Event Store`; `Event Store --subscription→ Projector container --SQL→ Read DB`; `Query API container --SQL→ Read DB`.
- **Công cụ:** Docker/Kubernetes, EventStoreDB/PostgreSQL, volume/backup và OpenTelemetry.
- **Các bước:** deploy Event Store → tạo schema → deploy Command API → deploy Read DB/Projector → replay → deploy Query API → kiểm tra end-to-end.
- **Bản in:** lệnh deploy, Event Store UI và log projector.

---

## Câu 15 — Event Sourcing: tiến trình xuất danh sách

### Đề bài rút gọn

- Chọn một chức năng xuất danh sách cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output.
- **Nộp kèm:** giao diện xem danh sách.

### Đáp án cốt lõi

- **Core:** Query API đọc danh sách từ Read Model đã được projector tính sẵn, không replay mỗi lần xem.
- **Process view:** `Event Store → Python Projector → PostgreSQL Read Model`; `User → UI --REST→ FastAPI Query API --SQL→ Read Model → JSON list → UI`.
- **Input:** token, filter và phân trang.
- **Xử lý:** kiểm quyền/tham số → query Read Model → tạo DTO.
- **Output:** danh sách, tổng số dòng và thông tin phân trang.
- **Bản in:** giao diện danh sách.

---

## Câu 16 — Event Sourcing: lưu trữ và tái tạo trạng thái

### Đề bài rút gọn

- Vẽ **storage view**.
- Liệt kê công cụ dùng để cài đặt thiết kế lưu trữ.
- Trình bày các bước cài đặt thiết kế lưu trữ.
- Vẽ luồng dữ liệu từ trạng thái ban đầu đến trạng thái cuối cùng.
- Giải thích cách tái tạo trạng thái hiện tại từ các event đã lưu.
- Liệt kê công cụ dùng để tái tạo trạng thái.
- Trình bày các bước tái tạo trạng thái.

### Đáp án cốt lõi

- **Core:** Event Store là nguồn sự thật; Read Model là dữ liệu được tạo lại từ events.
- **Storage view:** Event gồm `event_id`, `aggregate_id`, `version`, `type`, `payload`, `time`; Checkpoint lưu vị trí projector; Read Model lưu trạng thái hiện tại.
- **Công cụ/cài đặt:** EventStoreDB/PostgreSQL + migration; tạo event table/constraint → checkpoint/read tables → projector.
- **Luồng trạng thái:** `0 --Deposited(100)→ 100 --Withdrawn(30)→ 70`.
- **Tái tạo:** bắt đầu state rỗng/snapshot → đọc events đúng version → áp dụng tuần tự → nhận state cuối.
- **Rebuild Read Model:** tạo bảng mới → replay toàn bộ → so count/state → chuyển Query API sang bảng mới.
- **Công cụ tái tạo:** Event Store client, projector/rebuild script và DB viewer.

---

## Câu 17 — Event-Driven: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** producer phát event; broker chuyển/giữ event; consumer độc lập xử lý.
- **Khi dùng:** nhiều thành phần cần phản ứng bất đồng bộ với cùng sự kiện và cần tách producer khỏi consumer.
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

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án cốt lõi

- **Core:** broker và mỗi producer/consumer chạy thành process/container riêng.
- **Deployment view:** `Client --HTTPS→ Producer API container --SQL→ PostgreSQL/Outbox --event→ Kafka → Consumer containers --SQL→ Databases`.
- **Công cụ:** Docker/Kubernetes, PostgreSQL, Kafka/RabbitMQ và Grafana.
- **Các bước:** deploy broker/topic → deploy DB/consumers → deploy producer → gửi event test → kiểm tra kết quả/lag → scale consumer nếu cần.
- **Bản in:** lệnh deploy, broker UI và trạng thái consumers.

---

## Câu 19 — Event-Driven: tiến trình nhập dữ liệu

### Đề bài rút gọn

- Chọn một chức năng nhập dữ liệu cụ thể.
- Vẽ **process view** cho chức năng đó.
- Liệt kê và giải thích các công cụ kiểm tra tính hợp lệ của input.
- Trình bày từng bước kiểm tra input.
- Trình bày từng bước ghi dữ liệu khi input hợp lệ.

### Đáp án cốt lõi

- **Core:** chỉ input hợp lệ mới được lưu và tạo event.
- **Process view:** `User → API → Validate → DB + Outbox → Kafka → Consumer → Result DB`.
- **Công cụ kiểm tra:** Pydantic/JSON Schema kiểm cấu trúc; JWT middleware kiểm quyền; service/DB constraint kiểm business rule.
- **Input sai:** trả `400/401/403/422`, không lưu.
- **Input đúng:** ghi business data + outbox trong một transaction → commit → trả ID → relay publish event.
- **Consumer:** kiểm schema/duplicate → xử lý → lưu kết quả → lỗi thì retry/DLQ.

---

## Câu 20 — Event-Driven: logging, tracing và monitoring

### Đề bài rút gọn

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- Trình bày các bước log event từ lúc phát sinh đến lúc được xử lý.
- Trình bày các bước trace toàn bộ hành trình của event.
- Trình bày cách monitor event và các thành phần xử lý.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện hiển thị kết quả.

### Đáp án cốt lõi

- **Core:** theo dõi một event từ producer qua broker đến consumer bằng các ID chung.
- **View:** `Producer → Kafka → Consumers → OpenTelemetry Collector → [Loki | Jaeger | Prometheus] → Grafana`.
- **Công cụ:** OpenTelemetry, Loki, Jaeger, Prometheus và Grafana.
- **Các bước:** tạo `event_id/correlation_id` → đặt vào header → log lúc publish/consume/retry/DLQ → tạo spans → thu lag/error/DLQ metrics → hiển thị và cảnh báo.
- **Kiểm tra:** phát một event, tìm toàn bộ log/trace theo correlation ID và xem dashboard lag.
- **Bản in:** lệnh xem log, trace và dashboard.

---

## Câu 21 — Lambda hoặc Kappa: chất lượng và logic

### Đề bài rút gọn

- Chọn **một** kiến trúc: Lambda hoặc Kappa.
- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Liệt kê công cụ dùng để kiểm tra các đặc tính đó.
- Trình bày các bước kiểm tra.
- Vẽ **logic view** của kiến trúc đã chọn.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

### Đáp án cốt lõi

- **Core:** Kappa dùng một stream pipeline; muốn tính lại thì replay event log.
- **Khi dùng:** dữ liệu đến liên tục, báo cáo gần thời gian thực và event log được giữ đủ lâu để replay.
- **Near real time — Công cụ:** Kafka/Flink metrics; **cách đo:** event-to-report latency và lag.
- **Scalability — Công cụ:** Locust + Kafka/Flink; **cách đo:** events/giây trước/sau khi tăng partition/parallelism.
- **Fault tolerance — Công cụ:** checkpoint + Docker/Kubernetes; **cách đo:** restart processor mà không mất/trùng kết quả.
- **Replay/recovery — Công cụ:** consumer group mới + SQL; **cách đo:** replay vào DB mới cho count/sum đúng.
- **Correctness — Công cụ:** tập event chuẩn; **cách đo:** aggregate cuối đúng kể cả duplicate/out-of-order.
- **Logic view:** `Data source → Kafka log → Flink/Kafka Streams → Serving DB → Report API/Dashboard`.
- **Bản in:** giao diện nhập, Kafka UI, cây source và dashboard lag.

---

## Câu 22 — Lambda hoặc Kappa: tiến trình xuất báo cáo

### Đề bài rút gọn

- Sử dụng cùng kiến trúc Lambda hoặc Kappa đã chọn.
- Chọn một chức năng xuất báo cáo thống kê cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output của báo cáo.
- **Nộp kèm:** giao diện báo cáo và giao diện hiển thị dữ liệu thô của báo cáo.

### Đáp án cốt lõi

- **Core:** stream processor tính sẵn số liệu; Report API chỉ đọc Serving DB.
- **Process view:** `Raw events → Kafka → Flink Processor --SQL→ PostgreSQL Serving DB`; `User --REST→ Report API --SQL→ Serving DB → Chart/Table`.
- **Input:** event dữ liệu; yêu cầu báo cáo gồm user và khoảng ngày.
- **Xử lý:** validate/deduplicate → tính tổng theo ngày → lưu aggregate/checkpoint → API kiểm quyền và query.
- **Output:** bảng/biểu đồ và thời điểm cập nhật cuối.
- **Khôi phục:** processor chạy lại từ checkpoint; đổi công thức thì replay vào bảng mới.
- **Bản in:** giao diện báo cáo và dữ liệu thô tương ứng.

---

## Checklist trước khi thi

- Khái niệm có WHAT → HOW → WHY → WHEN.
- Logic view có trách nhiệm → quan hệ → công nghệ/ngôn ngữ.
- Deployment view có node → artifact/module → giao thức.
- Process view có input → biến đổi → output → công nghệ.
- Mỗi đặc tính chất lượng có công cụ → cách kiểm tra → metric.
- Chỉ nói điều đã thực hành và chuẩn bị đúng bản in liên quan.
