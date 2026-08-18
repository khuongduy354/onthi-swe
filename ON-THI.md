# Ôn thi vấn đáp Kiến trúc phần mềm — 22 câu

- **Đề gốc:** [PDF 22 câu hỏi vấn đáp](materials/22-cau-hoi-thi-kien-truc-phan-mem.pdf) — GV. TS. Ngô Huy Biên, 2026.
- **Cách dùng:** mỗi mục in đậm tương ứng với một ý bắt buộc trong câu hỏi; học đủ các bullet để không bỏ sót ý.
- **Stack minh họa:** React, FastAPI, PostgreSQL, Kafka, Pinecone, Docker/Kubernetes và OpenTelemetry/Grafana.
- **Lưu ý:** khi thi phải thay stack mẫu bằng đúng thành phần, công cụ, câu lệnh và kết quả của bài thực hành nhóm mình.

## Nhớ chung cho mọi câu

- **Logic view:** thành phần phần mềm nào, làm gì và liên hệ với nhau ra sao.
- **Deployment view:** artifact chạy trên máy, container, cluster hoặc dịch vụ nào; giao tiếp bằng giao thức gì.
- **Process view:** input → các bước xử lý/biến đổi → output; có nhánh lỗi.
- **Development view:** source code chia thành repo, thư mục và module nào.
- **Storage view:** lưu thực thể nào, khóa/quan hệ gì và mỗi nơi lưu dùng để làm gì.
- **Security view:** authentication, authorization, TLS, secret, network và audit nằm ở đâu.
- **Scalability view:** load balancer, replica, partition, cache và database được mở rộng thế nào.
- **Observability view:** log, metric và trace đi từ ứng dụng đến collector, backend và dashboard ra sao.
- **Khi nói về chất lượng:** luôn nêu `đặc tính → công cụ → cách thử → metric/kết quả`.
- **Khi vẽ:** box ghi tên thành phần/công nghệ; mũi tên ghi HTTPS, REST/gRPC, event hoặc dữ liệu.

---

## Câu 1 — Microservices: chất lượng và triển khai

- **Core:** chia hệ thống theo nghiệp vụ thành các service tự chủ, có thể phát triển, deploy và scale riêng.
- **Năm đặc tính — công cụ — cách đo:**
  - **1. Performance — Công cụ:** JMeter/Locust/k6 + Prometheus/Grafana; **cách đo:** tạo cùng một mức tải, ghi p95 latency, request/giây và error rate.
  - **2. Scalability — Công cụ:** Locust + `kubectl scale`/HPA; **cách đo:** chạy tải với 1 replica rồi 3 replica, so throughput, p95 và CPU; kết quả phải tốt hơn khi tăng replica.
  - **3. Availability — Công cụ:** `kubectl delete pod` + Prometheus; **cách đo:** xóa một pod khi đang có tải, đếm request lỗi và thời gian hệ thống phục vụ lại.
  - **4. Modifiability/deployability — Công cụ:** GitHub Actions + Kubernetes rollout; **cách đo:** đổi và deploy chỉ Search Service, kiểm tra service khác không build/deploy lại và downtime trong ngưỡng.
  - **5. Security — Công cụ:** Postman/pytest + OWASP ZAP; **cách đo:** không token phải `401`, sai quyền phải `403`, đúng quyền `2xx`, không còn lỗ hổng mức nghiêm trọng sau khi quét.
- **Deployment view:** `Browser → Nginx/Ingress → Kong Gateway → [Auth | Document | Search] pods → [PostgreSQL | Pinecone]`; `Document → Kafka → Index Worker pods`.
- **Công cụ theo thành phần:** React/CDN cho Web; Nginx/Kong cho edge; FastAPI + Docker/Kubernetes cho service; Kafka cho broker; PostgreSQL/Pinecone cho dữ liệu; Kubernetes Secret/Vault cho secret.
- **Các bước triển khai:** test/build → tạo image có version → push registry → deploy DB/broker → tạo secret/config → deploy API/worker/Ingress → chạy migration → kiểm tra health, log và E2E → rollback nếu lỗi.
- **Bản in:** sơ đồ; kết quả load test; `docker compose ps`/`kubectl get pods`; lệnh deploy và health check.

---

## Câu 2 — Microservices: logic, giao tiếp và tiến trình

- **Logic view:** `React Web → Kong/Nginx → [Auth Service | Document Service | Search Service]`; `Document Service → Kafka → Index Worker`; `Search Service → Pinecone`.
- **Trách nhiệm/công cụ:** Auth phát JWT; Document quản lý metadata trong PostgreSQL; Search truy vấn vector; Index Worker tách đoạn/embedding; các service dùng FastAPI/Python.
- **Giao tiếp đồng bộ:** REST/JSON hoặc gRPC khi cần kết quả ngay; dùng timeout, retry có backoff và circuit breaker.
- **Giao tiếp bất đồng bộ:** Kafka/RabbitMQ cho xử lý nền; event có schema/version và `event_id`; consumer phải idempotent.
- **Nguyên tắc dữ liệu:** mỗi service sở hữu dữ liệu của mình; service khác gọi API hoặc nhận event, không đọc trực tiếp bảng riêng.
- **Process view — upload tài liệu:** `User → React → Gateway → Document Service → PostgreSQL + Outbox → Kafka → Index Worker → Embedding API → Pinecone`.
- **Input/output:** input là file + JWT; API trả `202 + document_id`; kết quả cuối là tài liệu ở trạng thái `indexed` và tìm kiếm được.
- **Nhánh lỗi:** file/quyền sai trả `400/403`; worker lỗi thì retry, quá số lần vào DLQ.
- **Bản in:** cây source; lệnh clone/build/run; request/response API và log worker.

---

## Câu 3 — Microservices: bảo mật và mở rộng

- **Security view:** `Internet --HTTPS→ WAF/Gateway --JWT→ Services --TLS/private network→ Databases`; Secret Manager và Audit Log nối với các service.
- **Công cụ bảo mật:** Nginx/Kong cho TLS/rate limit; Keycloak/Auth0 cho OAuth2/JWT; FastAPI middleware cho authorization; NetworkPolicy cho mạng; PostgreSQL role cho quyền DB; Vault/Kubernetes Secret cho khóa.
- **Cơ chế:** authentication xác định ai; authorization kiểm tra được làm gì; TLS mã hóa khi truyền; DB mã hóa khi lưu; không ghi token/password vào source hoặc log.
- **Kiểm tra bảo mật:** không token → `401`; thiếu quyền → `403`; đúng quyền → `2xx`; quét OWASP ZAP và kiểm tra audit log.
- **Scalability view:** `Ingress/Load Balancer → nhiều API pods → Redis/PostgreSQL`; `Kafka partitions → nhiều worker trong consumer group`.
- **Công cụ mở rộng:** Kubernetes Deployment/HPA; Prometheus đo CPU/latency; Redis cache; PostgreSQL read replica; Kafka partition và consumer group.
- **Các bước scale:** load test baseline → tìm bottleneck → tăng đúng replica/partition/cache → chạy lại cùng tải → so latency, throughput, error rate và lag.
- **Lệnh minh họa:** `kubectl autoscale deployment search-service --cpu-percent=70 --min=2 --max=10`; `kubectl scale deployment search-service --replicas=3`; `kubectl get hpa,pods`.
- **Bản in:** cấu hình đã che secret; số pod/HPA trước-sau; lệnh thiết lập và thực hiện scale.

---

## Câu 4 — Microservices: logging và tracing

- **Log:** sự kiện/lỗi trong một service; **trace:** hành trình của một request qua nhiều service; **metric:** số liệu tổng hợp theo thời gian.
- **Observability view:** `Gateway → Service A → Service B → OpenTelemetry Collector → [Loki/ELK | Jaeger/Tempo | Prometheus] → Grafana/Alertmanager`.
- **Công cụ:** OpenTelemetry SDK tạo telemetry; Collector tiếp nhận/chuyển tiếp; Loki/ELK lưu log; Jaeger/Tempo lưu trace; Prometheus/Grafana lưu metric, dashboard và alert.
- **Dữ liệu cần ghi:** time, level, service, operation, status, duration, `trace_id`; không ghi password/token hoặc dữ liệu nhạy cảm.
- **Các bước cài:** thêm OTel SDK → instrument HTTP/DB → truyền trace context → export đến Collector → cấu hình backend/dashboard/alert.
- **Cách kiểm tra:** gửi một request → lấy `trace_id` → tìm log của mọi service → mở trace để xem span chậm/lỗi → tạo lỗi thử và kiểm tra alert.
- **Bản in:** `docker compose logs`/`kubectl logs`; log có trace ID; giao diện Jaeger và Grafana.

---

## Câu 5 — Microservices: phát triển, thay đổi và lưu trữ

- **Development view:**
  - `services/auth-service/`: đăng nhập và token.
  - `services/document-service/`: quản lý tài liệu.
  - `services/search-service/`: tìm kiếm.
  - `services/index-worker/`: xử lý event và embedding.
  - `shared-contracts/`: OpenAPI/JSON Schema/Avro.
  - `tests/`: contract, integration và E2E.
  - `deploy/`: Docker Compose/Kubernetes.
- **Ví dụ mở rộng:** thêm Notification Service nhận `DocumentIndexed` mà không sửa logic Search/Payment cũ.
- **Các bước thay đổi:** định nghĩa event tương thích ngược → tạo service mới → unit test → contract/integration test Kafka → E2E → build/deploy riêng bằng feature flag → theo dõi rồi mở toàn bộ.
- **Giảm ảnh hưởng:** service mới chỉ phụ thuộc event contract; không truy cập source/DB riêng của service khác; version contract và chạy regression test.
- **Storage view:** `User 1—N Document 1—N Chunk`; Document DB lưu metadata/owner/status; Pinecone lưu vector gắn `chunk_id`; Outbox lưu event chờ publish.
- **Mục đích thực thể:** User định danh; Document là tài liệu; Chunk là đoạn; Vector phục vụ semantic search; Outbox chống mất event giữa DB và Kafka.
- **Lệnh minh họa:** `docker compose build notification-service`; `docker compose run --rm notification-service pytest`; `docker compose up -d notification-service`.
- **Bản in:** cây thư mục; sơ đồ dữ liệu; lệnh test/build/deploy thành phần mới.

---

## Câu 6 — Micro-Frontends: chất lượng, logic, kết hợp và giao tiếp

- **Core:** chia frontend theo domain thành các MFE do các nhóm phát triển/deploy độc lập; App Shell ghép chúng thành một ứng dụng.
- **Logic view:** `Browser → App Shell → [Account MFE | Search MFE | Report MFE] → Backend API`; shared design system dùng chung.
- **Công cụ:** React/Vue; React Router; Webpack Module Federation/import map; npm design-system package; Storybook, Vitest và Playwright.
- **Đặc tính — công cụ — cách đo:**
  - **Deployability — Công cụ:** GitHub Actions/CDN; **cách đo:** sửa và deploy riêng Search MFE, kiểm tra pipeline và artifact của Shell/MFE khác không thay đổi.
  - **Fault isolation — Công cụ:** Chrome DevTools/Playwright; **cách đo:** chặn `remoteEntry.js`, Search hiện fallback nhưng Shell và route khác vẫn dùng được.
  - **Performance — Công cụ:** Lighthouse/Web Vitals + bundle analyzer; **cách đo:** ghi LCP, INP và kích thước JS của trang tổng hợp, so với budget đã đặt.
  - **Consistency — Công cụ:** Storybook/visual regression; **cách đo:** so ảnh giao diện với baseline, số visual diff ngoài dự kiến phải bằng 0.
  - **Testability — Công cụ:** Vitest/Storybook/Playwright; **cách đo:** component test từng MFE và E2E từ Shell đều pass, theo dõi coverage nếu nhóm có đặt ngưỡng.
- **Cách kết hợp:** Shell tải remote runtime bằng Module Federation, đặt component vào route/layout, có loading/error boundary và khóa version dependency dùng chung.
- **Cách giao tiếp:** props/callback cho quan hệ gần; URL/router cho navigation; event bus cho sự kiện đơn giản; backend là nguồn dữ liệu chung; tránh global mutable state lớn.
- **Bản in:** giao diện từng MFE, Storybook và trang tổng hợp toàn hệ thống.

---

## Câu 7 — Micro-Frontends: triển khai

- **Deployment view:** `Repo từng MFE → GitHub Actions → S3/Netlify/Vercel/CDN`; `Browser → Shell → manifest/import map → remoteEntry.js → Backend API`.
- **Công cụ theo thành phần:** GitHub/GitLab lưu source; npm/Vite/Webpack build; CI chạy test; CDN lưu artifact có hash/version; manifest ánh xạ MFE tới URL; Module Federation ghép trong browser.
- **Các bước:** lint/test/build từng MFE → upload artifact version mới nhưng giữ version cũ → cấu hình HTTPS/CORS/cache → cập nhật manifest ở preview → E2E từ Shell → canary production → monitor lỗi/Web Vitals → rollback manifest nếu lỗi.
- **Lệnh minh họa:** `npm ci`; `npm test`; `npm run build`; `aws s3 sync dist/ s3://<bucket>/<mfe>/<version>/`.
- **Bản in:** CI log; lệnh build/upload; giao diện CDN/hosting và trang sau deploy.

---

## Câu 8 — JAMstack: chất lượng và logic

- **Core:** JavaScript tạo tương tác, API cung cấp dữ liệu động, Markup được tạo trước khi build và phát từ CDN.
- **Logic view:** `Git/Headless CMS → Next.js/Astro build → HTML/CSS/JS → CDN → Browser`; `Browser → Serverless/FastAPI` cho phần động.
- **Công cụ:** Markdown/Contentful; Next.js/Astro; GitHub Actions; Netlify/Vercel/S3 + CloudFront; Lighthouse/k6.
- **Đặc tính — công cụ — cách đo:**
  - **Performance — Công cụ:** Lighthouse/WebPageTest; **cách đo:** ghi LCP, TTFB, tổng kích thước tải và cache hit/header của trang từ CDN.
  - **Scalability — Công cụ:** k6/Locust + dashboard CDN; **cách đo:** tăng virtual users, ghi request/giây, p95 và error rate trong khi không tăng origin server.
  - **Availability — Công cụ:** curl/Playwright + uptime monitor; **cách đo:** tắt API/origin, trang tĩnh vẫn trả `200` và phần động hiển thị fallback.
  - **Security — Công cụ:** OWASP ZAP + secret scanner; **cách đo:** số lỗi nghiêm trọng bằng 0, bundle không chứa API key, API vẫn trả `401/403` khi sai quyền.
  - **Deployability/freshness — Công cụ:** GitHub Actions + Netlify/Vercel; **cách đo:** đổi content, ghi thời gian commit-to-live, xác nhận nội dung mới và thử rollback về deployment trước.
- **Cây source:** `src/pages/`, `src/components/`, `content/`, `public/`, `src/api/`, file cấu hình build.
- **Bản in:** giao diện; cây thư mục; log/kết quả `npm run build`.

---

## Câu 9 — RAG: chất lượng và logic

- **Core:** tìm các đoạn tài liệu liên quan rồi đưa chúng vào context để LLM trả lời có căn cứ.
- **Indexing view:** `Documents → Loader/Clean → Chunk → Embedding API → Pinecone/FAISS`.
- **Query view:** `Question → Query embedding → top-k + ACL filter → Prompt(question + chunks) → LLM → Answer + citations`.
- **Công cụ:** LangChain/LlamaIndex/Python cho loader/chunker; embedding/LLM API; Pinecone/FAISS; FastAPI Query API; React UI.
- **Đặc tính — công cụ — cách đo:**
  - **Retrieval relevance — Công cụ:** bộ câu hỏi/chunk gán nhãn + script eval; **cách đo:** tính Hit-rate/Recall@k/MRR và kiểm tra relevant chunk có trong top-k.
  - **Correctness/faithfulness — Công cụ:** đáp án chuẩn + RAGAS/LLM judge và kiểm tra tay; **cách đo:** tỷ lệ câu đúng/có căn cứ, câu ngoài tài liệu phải từ chối thay vì bịa.
  - **Citation correctness — Công cụ:** citation checker/pytest; **cách đo:** mở từng citation, tính tỷ lệ nguồn thật sự chứa đoạn hỗ trợ câu trả lời.
  - **Performance — Công cụ:** Locust/k6 + OpenTelemetry; **cách đo:** p95 retrieval latency, LLM latency, end-to-end latency và error rate.
  - **Freshness/reliability — Công cụ:** worker logs + Pinecone UI; **cách đo:** thời gian từ lúc thêm/sửa/xóa tài liệu đến lúc truy vấn thấy thay đổi; job lỗi phải retry và không tạo vector trùng.
  - **Security — Công cụ:** pytest/Postman với hai tài khoản; **cách đo:** số chunk của tenant B xuất hiện trong kết quả tenant A phải bằng 0.
- **Cây source:** `web/`, `query_api/`, `indexing/`, `shared/schemas/`, `tests/`, `deploy/`.
- **Bản in:** giao diện hỏi đáp/citation; top-k hoặc vector metadata; cây source.

---

## Câu 10 — RAG: triển khai

- **Deployment view:** `Browser → Web/CDN → Query API pod → [Embedding API | LLM API | Pinecone]`; `Data sources → Crawler → Kafka/Temporal → Index Worker → Pinecone`; tất cả → OTel/Grafana.
- **Artifact/công cụ:** Web static bundle; Docker images cho Query API/Crawler/Worker; Kubernetes; Kafka/Temporal; managed Pinecone/LLM; Secret/ConfigMap.
- **Các bước:** tạo vector index đúng dimension → cấu hình namespace/ACL → lưu API keys trong Secret → build/push images → deploy queue/crawler/worker → index dữ liệu mẫu → kiểm tra vector/metadata → deploy Query API/Web → test câu biết/không biết đáp án và phân quyền → index toàn bộ.
- **Vận hành:** đặt timeout, retry, DLQ, probe, autoscaling, log/trace; rollback image hoặc rebuild index khi lỗi.
- **Bản in:** lệnh deploy; trạng thái containers/pods; Pinecone UI; log worker và giao diện query.

---

## Câu 11 — LLM-based Agent: chất lượng và logic

- **Core:** agent lặp `quan sát trạng thái → LLM chọn hành động/tool → chạy tool → đọc kết quả` đến khi hoàn thành hoặc chạm giới hạn.
- **Logic view:** `User → Chat UI → Agent Orchestrator ↔ LLM`; `Orchestrator → Permission Check → Tool Registry → Tool Result`; Memory/Checkpoint/Audit nối với Orchestrator.
- **Công cụ:** React; LangGraph/custom Python; JSON Schema/Pydantic cho tool; PostgreSQL/Redis cho state; OpenTelemetry cho audit/trace; LLM API.
- **Đặc tính — công cụ — cách đo:**
  - **Correctness — Công cụ:** bộ task chuẩn + pytest/eval harness; **cách đo:** task success rate và tỷ lệ tool sequence/kết quả đúng mong đợi.
  - **Safety/security — Công cụ:** red-team prompts + policy tests; **cách đo:** request thiếu quyền/prompt injection/write tool bị chặn hoặc yêu cầu approval, số lần truy cập trái phép bằng 0.
  - **Bounded execution/cost — Công cụ:** telemetry của LLM + cấu hình agent; **cách đo:** task cố tạo loop phải dừng ở `max_steps`, timeout hoặc token/cost budget.
  - **Reliability — Công cụ:** mock server + workflow/checkpoint DB; **cách đo:** tool trả timeout/5xx phải retry/resume đúng, side effect chỉ xảy ra một lần.
  - **Observability — Công cụ:** OpenTelemetry/Jaeger; **cách đo:** mỗi model/tool call có span, latency, token và cost; log không lộ secret.
  - **Modifiability — Công cụ:** contract test cho tool schema; **cách đo:** thêm Calculator và chạy test thành công mà không sửa core agent loop.
- **Cây source:** `web/`, `agent/`, `tools/`, `policy/`, `storage/`, `tests/`, `deploy/`.
- **Bản in:** giao diện agent; cây source; một run/tool call thành công và thất bại.

---

## Câu 12 — LLM-based Agent: triển khai

- **Deployment view:** `Client → Gateway/Auth → Agent API → Temporal/Kafka → Agent Workers → [LLM | RAG | Tool Gateway → External APIs]`; Worker → Checkpoint DB, Secrets và OTel/Grafana.
- **Công cụ theo node:** Kong/Keycloak; FastAPI/Docker/Kubernetes; Temporal/Kafka; PostgreSQL; Vault/Kubernetes Secret; OpenTelemetry/Jaeger/Grafana.
- **Các bước:** định nghĩa tool schema/quyền → lưu secret → build/push API/Worker images → deploy DB và queue → deploy Gateway/API/Tool Gateway/Workers → cấu hình probe/autoscale → đặt max steps/timeout/retry/approval/cost limit → test staging bằng mock/read-only tools → canary → monitor và rollback nếu lỗi.
- **Bản in:** lệnh/status deploy; trạng thái worker; trace một agent run và giao diện công cụ trực tuyến nếu dùng.

---

## Câu 13 — Event Sourcing: chất lượng và logic

- **Core:** events bất biến là nguồn sự thật; trạng thái hiện tại được tính bằng cách áp dụng events theo thứ tự.
- **Logic view:** `UI → Command API → Aggregate/rules → Event Store → Projector → Read Model ← Query API ← UI`.
- **Công cụ:** React; FastAPI; EventStoreDB/PostgreSQL append-only; Python projector; PostgreSQL Read Model; pytest/Locust.
- **Ví dụ:** `score=0 → QuizAnswered(+10) → AnswerCorrected(-2) → score=8`.
- **Đặc tính — công cụ — cách đo:**
  - **Auditability — Công cụ:** EventStoreDB UI/SQL; **cách đo:** mỗi thay đổi có event gồm actor/time/type/payload, role ứng dụng không thể `UPDATE/DELETE` event.
  - **Recoverability — Công cụ:** projector rebuild script + DB query; **cách đo:** xóa Read Model rồi replay, count/state/hash sau rebuild phải bằng trước đó.
  - **Extensibility — Công cụ:** projector framework + integration test; **cách đo:** tạo report/projection mới từ event cũ mà Command API và event history không đổi.
  - **Performance — Công cụ:** Locust/k6 + Prometheus; **cách đo:** append p95/throughput, query p95 và projection lag dưới ngưỡng bài thực hành.
  - **Consistency/reliability — Công cụ:** pytest concurrent/duplicate tests; **cách đo:** duplicate chỉ tạo một kết quả, hai command cùng version thì một command bị từ chối bởi `expected_version`.
- **Luồng:** Command API nạp stream → Aggregate kiểm rule → append event với version → Projector cập nhật Read Model idempotently → Query API đọc model.
- **Cây source:** `command_api/`, `domain/`, `projections/`, `query_api/`, `migrations/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; event rows/EventStoreDB UI; cây source.

---

## Câu 14 — Event Sourcing: triển khai

- **Deployment view:** `Browser → Ingress → Command API pods → EventStoreDB + volume`; `EventStoreDB → Projector pods → PostgreSQL Read DB`; `Browser → Query API pods → Read DB`; tất cả → OTel/Grafana.
- **Công cụ:** Docker/Kubernetes; EventStoreDB/PostgreSQL; volume/backup; Kubernetes Secret; OpenTelemetry/Grafana/Jaeger.
- **Các bước:** deploy Event Store có TLS/auth/backup → tạo event schema/role → deploy Read DB và migration → deploy Command API, test append/version → deploy Projector, replay và chờ lag về 0 → deploy Query API/Ingress → chạy E2E command-event-projection-query → kiểm tra backup/log/metric → rollback service nếu lỗi, không sửa event.
- **Bản in:** lệnh deploy; trạng thái pod/container; Event Store UI; log và trạng thái projector.

---

## Câu 15 — Event Sourcing: tiến trình xuất danh sách

- **Process view:** `Event Store → Projector → Read Model`; khi xem: `User → React UI → Query API → PostgreSQL Read Model → DTO/JSON → UI`.
- **Input:** JWT/user ID, filter, page, page size và sort.
- **Các bước:** xác thực quyền → validate tham số → `SELECT` read model với index/pagination → map row thành DTO → trả kết quả.
- **Output:** `items`, `total`, `page`, `page_size` và có thể `last_projected_position`.
- **Nhánh lỗi:** sai input/quyền → `400/403`; lỗi DB → `5xx` + log/trace.
- **Điểm cần giải thích:** không replay mọi event khi user mở danh sách vì chậm; projector tạo sẵn model nên query nhanh nhưng có thể chậm cập nhật ngắn do eventual consistency.
- **Công cụ:** React; FastAPI/Pydantic; PostgreSQL; OpenTelemetry.
- **Bản in:** giao diện danh sách và rows tương ứng trong Read Model.

---

## Câu 16 — Event Sourcing: lưu trữ và tái tạo trạng thái

- **Storage view:**
  - `Domain Event`: `event_id`, `aggregate_id`, `version`, `event_type`, `schema_version`, `payload`, `occurred_at`, `global_position`.
  - Ràng buộc: `event_id` unique; `(aggregate_id, version)` unique; event chỉ append.
  - `Projector Checkpoint`: tên projector + vị trí cuối đã đọc.
  - `Read Model`: state dẫn xuất, tối ưu cho query.
  - `Processed Event`: chống consumer xử lý trùng; `Snapshot`: tùy chọn để nạp stream nhanh hơn.
- **Công cụ lưu trữ:** EventStoreDB hoặc PostgreSQL append-only; Alembic/Flyway; Python projector; `psql`/DB UI; volume và backup.
- **Các bước cài storage:** tạo Event Store/role/backup → tạo schema/constraint → tạo Read DB/index/checkpoint → cài append với `expected_version` → cài projector idempotent → seed/test thứ tự, restart và restore.
- **Luồng trạng thái:** `score=0 --QuizAnswered(+10)→ 10 --QuizAnswered(+8)→ 18 --AnswerCorrected(-2)→ 16`.
- **Tái tạo một aggregate:** bắt đầu state rỗng/snapshot → đọc event đúng version → gọi `apply(state,event)` tuần tự → state cuối là hiện tại; thiếu version thì dừng/báo lỗi.
- **Rebuild toàn bộ:** tạo `read_model_v2` → reset checkpoint v2 → replay theo `global_position` → so count/sum/hash với model cũ → lag về 0 → chuyển Query API sang v2 → giữ v1 để rollback.
- **Công cụ tái tạo:** EventStoreDB/PostgreSQL client; rebuild script; checkpoint; `psql`/DB viewer; metric projection lag.
- **Bản in nên có:** events trước replay; lệnh rebuild; Read Model sau replay và kết quả đối chiếu.

---

## Câu 17 — Event-Driven: chất lượng và logic

- **Core:** producer phát sự kiện đã xảy ra; broker giữ/chuyển event; các consumer độc lập đăng ký và xử lý.
- **Logic view:** `Upload UI → Document API → PostgreSQL + Outbox → Kafka → [Extractor | Audit | Notification]`; `Extractor → TextExtracted → Kafka → Indexer → Pinecone`.
- **Công cụ:** React; FastAPI/Node; PostgreSQL; Kafka/RabbitMQ; Python consumers; JSON Schema/Avro; OpenTelemetry/Grafana.
- **Đặc tính — công cụ — cách đo:**
  - **Loose coupling — Công cụ:** Git diff/CI + contract test; **cách đo:** thêm Audit Consumer, producer source/build không đổi và event contract vẫn pass.
  - **Scalability/performance — Công cụ:** Locust/k6 + Kafka/Grafana; **cách đo:** events/giây và consumer lag trước/sau khi tăng partition + consumer.
  - **Availability/durability — Công cụ:** Docker/Kubernetes + Kafka UI; **cách đo:** tắt consumer, phát event, bật lại; toàn bộ event tồn đọng phải được xử lý.
  - **Reliability — Công cụ:** fault injection + outbox/DLQ dashboard; **cách đo:** crash sau DB commit không làm mất event, lỗi tạm thời được retry, lỗi vĩnh viễn vào DLQ.
  - **Idempotency/consistency — Công cụ:** pytest/Postman + DB query; **cách đo:** gửi cùng `event_id` hai lần nhưng business result chỉ thay đổi một lần.
  - **Observability — Công cụ:** OpenTelemetry/Jaeger/Grafana; **cách đo:** tìm đủ producer và consumer spans theo `correlation_id`, dashboard hiển thị lag/retry/DLQ.
- **Cây source:** `producer_api/`, `outbox_relay/`, `consumers/`, `contracts/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; broker/topic UI; cây source.

---

## Câu 18 — Event-Driven: triển khai

- **Deployment view:** `Client → Ingress → Producer API pods → PostgreSQL + Outbox → Relay → Kafka topics/DLQ → Consumer pods → Databases`; tất cả → OTel/Prometheus/Grafana.
- **Công cụ:** Docker/Kubernetes; Nginx/Ingress; PostgreSQL; Debezium/polling relay; Kafka/RabbitMQ; Pinecone; Secret; OpenTelemetry/Grafana.
- **Các bước:** deploy broker/topic/DLQ → cấu hình replication, retention, ACL → deploy result DB và consumers → deploy business DB/outbox relay → deploy producer API → gửi event test → kiểm tra từng consumer/result → monitor lag/retry/DLQ → tăng partition/consumer nếu cần → test rollback consumer độc lập.
- **Bản in:** lệnh deploy/scale; trạng thái containers/pods; Kafka UI; log và trạng thái consumers.

---

## Câu 19 — Event-Driven: tiến trình nhập và kiểm tra dữ liệu

- **Process view:** `User → React form → FastAPI validation → PostgreSQL transaction[business row + outbox] → Relay → Kafka → Consumer → Result DB`.
- **Input:** JSON/file, JWT và idempotency key.
- **Kiểm tra hợp lệ/công cụ:**
  - React kiểm tra UX; server vẫn kiểm tra lại.
  - Pydantic/JSON Schema kiểm required/type/range/format; sai → `400/422`.
  - JWT middleware xác thực; policy kiểm role/owner; sai → `401/403`.
  - Service + PostgreSQL kiểm business rule, foreign key và unique constraint; sai → `409/422`.
- **Ghi dữ liệu hợp lệ:** trong một DB transaction ghi business row + outbox event; commit xong mới trả `202 + id`; lỗi thì rollback cả hai.
- **Publish:** Debezium/polling relay gửi outbox lên Kafka; crash sau DB commit không mất event vì outbox row còn đó.
- **Consumer:** validate schema/version → kiểm `event_id` → ghi result + processed-event trong transaction → commit offset sau DB commit.
- **Nhánh lỗi:** lỗi tạm thời retry có backoff; lỗi vĩnh viễn/quá số lần vào DLQ và phát cảnh báo.
- **Các test:** input sai không tạo row/event; duplicate chỉ tạo một kết quả; crash sau commit vẫn publish; poison event vào DLQ.

---

## Câu 20 — Event-Driven: logging, tracing và monitoring

- **Observability view:** `Producer --event headers→ Kafka → Consumers → OTel Collector → [Loki/ELK | Jaeger/Tempo | Prometheus] → Grafana/Alertmanager`.
- **ID cần truyền:** `event_id` nhận diện event; `correlation_id` nhóm một nghiệp vụ; `traceparent` nối trace context; đặt trong message header.
- **Công cụ:** OTel SDK; Kafka headers; OTel Collector; Loki/ELK; Jaeger/Tempo; Prometheus; Grafana/Alertmanager.
- **Các bước:** producer tạo IDs/span và log lúc ghi outbox/publish → consumer extract context và tạo process span → log nhận/thành công/retry/DLQ → thu event rate, duration, lag, retry, DLQ size → export qua Collector → tạo dashboard/alert.
- **Log fields:** time, service, topic, partition, offset, status, duration và các ID; không log token/payload nhạy cảm.
- **Kiểm tra:** phát một event → tìm mọi log/trace theo correlation ID → xem producer và từng consumer → tạo consumer lỗi → kiểm tra retry, DLQ và alert.
- **Bản in:** lệnh xem log; log có IDs; trace Jaeger; dashboard lag/retry/DLQ.

---

## Câu 21 — Kappa: chất lượng và logic

- **Lựa chọn:** đề cho chọn Lambda hoặc Kappa; chọn **Kappa** và trình bày nhất quán Kappa.
- **Core:** chỉ có một stream pipeline cho dữ liệu mới và việc tính lại; khi đổi logic thì replay durable event log.
- **Logic view:** `React/FastAPI → Kafka event log → Flink/Kafka Streams → PostgreSQL/ClickHouse Serving DB → Report API → Dashboard`; logic mới: `Kafka → Processor v2 → Serving DB v2`.
- **Công cụ:** Kafka; Flink/Kafka Streams; PostgreSQL/ClickHouse; FastAPI/React/Grafana; Prometheus/Locust.
- **Đặc tính — công cụ — cách đo:**
  - **Near real time — Công cụ:** Kafka/Flink metrics + Prometheus; **cách đo:** event-time đến serving-time latency, throughput và consumer lag.
  - **Scalability — Công cụ:** Locust + Kafka partition/Flink parallelism; **cách đo:** chạy cùng tải trước/sau khi tăng parallelism, so events/giây và lag.
  - **Fault tolerance — Công cụ:** Docker/Kubernetes + Flink checkpoint; **cách đo:** kill/restart processor, kết quả phải tiếp tục từ checkpoint và không mất/trùng.
  - **Replay/recovery — Công cụ:** Kafka consumer group mới + SQL; **cách đo:** replay vào DB v2, count/sum/hash phải khớp kết quả chuẩn.
  - **Evolvability — Công cụ:** processor v1/v2 + comparison script; **cách đo:** chạy song song từ cùng log, so output rồi mới chuyển Report API.
  - **Correctness — Công cụ:** tập raw events chuẩn + integration test; **cách đo:** aggregate/window cuối đúng với event bình thường, duplicate và out-of-order.
- **Khác Lambda:** Kappa không có batch layer riêng nên ít pipeline hơn; phải giữ event log đủ lâu để replay.
- **Cây source:** `producer/`, `contracts/`, `stream_processor/`, `report_api/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; Kafka UI; cây source; dashboard latency/lag.

---

## Câu 22 — Kappa: tiến trình xuất báo cáo thống kê

- **Process view:** `AnswerSubmitted → Kafka raw topic → Flink/Kafka Streams → Serving DB → Report API → Report UI`.
- **Input event:** `event_id`, `user_id`, `correct`, `event_time`; input report là JWT, user, khoảng ngày và timezone.
- **Biến đổi stream:** parse/validate schema → deduplicate `event_id` → gán daily window/timezone → tính `total`, `correct`, `accuracy` → upsert aggregate + checkpoint.
- **Xuất báo cáo:** Report API xác thực/validate filter → query số liệu đã tính sẵn bằng index user/date → trả JSON → UI vẽ bảng/biểu đồ.
- **Output:** số liệu mỗi ngày, tổng/đúng/accuracy và `last_processed_at` để biết độ mới.
- **Nhánh lỗi:** sai filter/quyền → `400/403`; event lỗi → DLQ; processor chết → restart từ checkpoint; duplicate không được cộng hai lần.
- **Event đến trễ:** xử lý theo watermark/window policy; nếu bài thực hành chỉ dùng processing time thì nói đúng giới hạn đó.
- **Đổi công thức:** replay Kafka vào bảng v2 → so kết quả → chuyển Report API → giữ bảng cũ để rollback.
- **Bản in:** giao diện báo cáo; Kafka UI/console chứa raw events; rows tương ứng trong Serving DB.

---

## Checklist 10 phút trên giấy A4

- **Đúng view:** logic, deployment, process, storage, security, scalability hoặc observability theo đề.
- **Đủ nhãn:** trách nhiệm của box; giao thức/dữ liệu trên mũi tên; công cụ cạnh thành phần.
- **Đủ quy trình:** bước đầu → xử lý → kết quả → nhánh lỗi/khôi phục.
- **Đủ chất lượng:** tên đặc tính → cách thử → metric/kết quả.
- **Đủ bằng chứng:** chọn đúng bản in mà câu hỏi yêu cầu.
