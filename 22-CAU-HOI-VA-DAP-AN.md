# 22 câu hỏi và đáp án ôn thi Kiến trúc phần mềm

- **Đề gốc:** [PDF 22 câu hỏi vấn đáp](materials/22-cau-hoi-thi-kien-truc-phan-mem.pdf) — GV. TS. Ngô Huy Biên, 2026.
- Mỗi câu gồm **đề bài rút gọn** và **đáp án gợi ý** ngay bên dưới.
- Khi thi, thay công cụ minh họa bằng đúng công nghệ, câu lệnh và kết quả của bài thực hành nhóm mình.

## Kiến thức chung

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

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Liệt kê công cụ có thể dùng để kiểm tra các đặc tính đó.
- Trình bày các bước kiểm tra.
- Vẽ **deployment view**.
- Ghi công cụ triển khai cho từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** giao diện/câu lệnh kiểm tra chất lượng và câu lệnh triển khai.

### Đáp án gợi ý

- **Core:** chia hệ thống theo nghiệp vụ thành các service tự chủ, có thể phát triển, deploy và scale riêng.
- **Đặc tính chất lượng:**
  - **Performance:** p95 latency thấp, throughput cao, error rate trong ngưỡng.
  - **Scalability:** thêm replica cho đúng service đang nghẽn.
  - **Availability/resilience:** một pod chết, pod khác vẫn phục vụ.
  - **Modifiability/deployability:** đổi một service mà không deploy toàn hệ thống.
  - **Security/observability:** đúng quyền, mã hóa và truy vết được lỗi.
- **Công cụ và cách kiểm tra:**
  - JMeter/Locust/k6 tạo tải; Prometheus/Grafana đo latency, throughput, CPU và lỗi.
  - Tắt một pod để đo failover; tăng replica rồi chạy lại cùng bài test.
  - OWASP ZAP và test JWT kiểm tra bảo mật; Jaeger tìm request theo `trace_id`.
- **Deployment view:** `Browser → Nginx/Ingress → Kong Gateway → [Auth | Document | Search] pods → [PostgreSQL | Pinecone]`; `Document → Kafka → Index Worker pods`.
- **Công cụ theo thành phần:** React/CDN cho Web; Nginx/Kong cho edge; FastAPI + Docker/Kubernetes cho service; Kafka cho broker; PostgreSQL/Pinecone cho dữ liệu; Kubernetes Secret/Vault cho secret.
- **Các bước triển khai:** test/build → tạo image có version → push registry → deploy DB/broker → tạo secret/config → deploy API/worker/Ingress → chạy migration → kiểm tra health, log và E2E → rollback nếu lỗi.
- **Bản in:** sơ đồ; kết quả load test; `docker compose ps`/`kubectl get pods`; lệnh deploy và health check.

---

## Câu 2 — Microservices: logic, giao tiếp và tiến trình

### Đề bài rút gọn

- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách các service giao tiếp với nhau.
- Vẽ **process view** cho một use case cụ thể.
- **Nộp kèm:** câu lệnh cài đặt mã nguồn hệ thống.

### Đáp án gợi ý

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

### Đề bài rút gọn

- Vẽ **security view**.
- Ghi công cụ dùng để cài đặt bảo mật cho từng thành phần.
- Vẽ **scalability view**.
- Ghi công cụ dùng để mở rộng từng thành phần.
- **Nộp kèm:** câu lệnh thiết lập khả năng mở rộng và câu lệnh thực hiện scale hệ thống.

### Đáp án gợi ý

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

### Đề bài rút gọn

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện kết quả thu được.

### Đáp án gợi ý

- **Log:** sự kiện/lỗi trong một service; **trace:** hành trình của một request qua nhiều service; **metric:** số liệu tổng hợp theo thời gian.
- **Observability view:** `Gateway → Service A → Service B → OpenTelemetry Collector → [Loki/ELK | Jaeger/Tempo | Prometheus] → Grafana/Alertmanager`.
- **Công cụ:** OpenTelemetry SDK tạo telemetry; Collector tiếp nhận/chuyển tiếp; Loki/ELK lưu log; Jaeger/Tempo lưu trace; Prometheus/Grafana lưu metric, dashboard và alert.
- **Dữ liệu cần ghi:** time, level, service, operation, status, duration, `trace_id`; không ghi password/token hoặc dữ liệu nhạy cảm.
- **Các bước cài:** thêm OTel SDK → instrument HTTP/DB → truyền trace context → export đến Collector → cấu hình backend/dashboard/alert.
- **Cách kiểm tra:** gửi một request → lấy `trace_id` → tìm log của mọi service → mở trace để xem span chậm/lỗi → tạo lỗi thử và kiểm tra alert.
- **Bản in:** `docker compose logs`/`kubectl logs`; log có trace ID; giao diện Jaeger và Grafana.

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

### Đáp án gợi ý

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

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách kết hợp các giao diện thành hệ thống hoàn chỉnh.
- Giải thích cách các giao diện giao tiếp với nhau.
- **Nộp kèm:** giao diện từng Micro-Frontend và giao diện tổng hợp.

### Đáp án gợi ý

- **Core:** chia frontend theo domain thành các MFE do các nhóm phát triển/deploy độc lập; App Shell ghép chúng thành một ứng dụng.
- **Logic view:** `Browser → App Shell → [Account MFE | Search MFE | Report MFE] → Backend API`; shared design system dùng chung.
- **Công cụ:** React/Vue; React Router; Webpack Module Federation/import map; npm design-system package; Storybook, Vitest và Playwright.
- **Đặc tính và kiểm tra:**
  - Deployability: sửa/build/deploy riêng Search MFE; Shell/MFE khác không build lại.
  - Fault isolation: chặn `remoteEntry.js`; Shell phải hiện fallback, route khác vẫn chạy.
  - Performance: Lighthouse/Web Vitals và bundle analyzer đo LCP/INP/kích thước JS.
  - Consistency/testability: Storybook visual test và E2E toàn Shell.
- **Cách kết hợp:** Shell tải remote runtime bằng Module Federation, đặt component vào route/layout, có loading/error boundary và khóa version dependency dùng chung.
- **Cách giao tiếp:** props/callback cho quan hệ gần; URL/router cho navigation; event bus cho sự kiện đơn giản; backend là nguồn dữ liệu chung; tránh global mutable state lớn.
- **Bản in:** giao diện từng MFE, Storybook và trang tổng hợp toàn hệ thống.

---

## Câu 7 — Micro-Frontends: triển khai

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh triển khai.

### Đáp án gợi ý

- **Deployment view:** `Repo từng MFE → GitHub Actions → S3/Netlify/Vercel/CDN`; `Browser → Shell → manifest/import map → remoteEntry.js → Backend API`.
- **Công cụ theo thành phần:** GitHub/GitLab lưu source; npm/Vite/Webpack build; CI chạy test; CDN lưu artifact có hash/version; manifest ánh xạ MFE tới URL; Module Federation ghép trong browser.
- **Các bước:** lint/test/build từng MFE → upload artifact version mới nhưng giữ version cũ → cấu hình HTTPS/CORS/cache → cập nhật manifest ở preview → E2E từ Shell → canary production → monitor lỗi/Web Vitals → rollback manifest nếu lỗi.
- **Lệnh minh họa:** `npm ci`; `npm test`; `npm run build`; `aws s3 sync dist/ s3://<bucket>/<mfe>/<version>/`.
- **Bản in:** CI log; lệnh build/upload; giao diện CDN/hosting và trang sau deploy.

---

## Câu 8 — JAMstack: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án gợi ý

- **Core:** JavaScript tạo tương tác, API cung cấp dữ liệu động, Markup được tạo trước khi build và phát từ CDN.
- **Logic view:** `Git/Headless CMS → Next.js/Astro build → HTML/CSS/JS → CDN → Browser`; `Browser → Serverless/FastAPI` cho phần động.
- **Công cụ:** Markdown/Contentful; Next.js/Astro; GitHub Actions; Netlify/Vercel/S3 + CloudFront; Lighthouse/k6.
- **Đặc tính và kiểm tra:**
  - Performance: Lighthouse/WebPageTest đo LCP/TTFB và cache header.
  - Scalability: k6/Locust load test URL CDN.
  - Availability: tắt API, phần tĩnh vẫn mở và phần động có fallback.
  - Security: quét ZAP, kiểm tra không có secret trong bundle; API vẫn authn/authz.
  - Deployability/freshness: đổi content → build/publish → kiểm tra nội dung → rollback deployment cũ.
- **Cây source:** `src/pages/`, `src/components/`, `content/`, `public/`, `src/api/`, file cấu hình build.
- **Bản in:** giao diện; cây thư mục; log/kết quả `npm run build`.

---

## Câu 9 — RAG: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án gợi ý

- **Core:** tìm các đoạn tài liệu liên quan rồi đưa chúng vào context để LLM trả lời có căn cứ.
- **Indexing view:** `Documents → Loader/Clean → Chunk → Embedding API → Pinecone/FAISS`.
- **Query view:** `Question → Query embedding → top-k + ACL filter → Prompt(question + chunks) → LLM → Answer + citations`.
- **Công cụ:** LangChain/LlamaIndex/Python cho loader/chunker; embedding/LLM API; Pinecone/FAISS; FastAPI Query API; React UI.
- **Đặc tính và kiểm tra:**
  - Retrieval relevance: bộ câu hỏi gán nhãn; đo Hit-rate/Recall@k/MRR và xem top-k.
  - Correctness/faithfulness: so đáp án chuẩn; hỏi ngoài tài liệu thì phải từ chối/ghi không đủ dữ kiện.
  - Citation: mở từng nguồn và đối chiếu đúng đoạn hỗ trợ.
  - Performance: Locust/k6 đo p95 retrieval và end-to-end latency.
  - Freshness/reliability: thêm/sửa/xóa tài liệu; kiểm tra re-index, retry và không trùng vector.
  - Security: user A không retrieve chunk của user B; ACL phải lọc trước khi gửi context cho LLM.
- **Cây source:** `web/`, `query_api/`, `indexing/`, `shared/schemas/`, `tests/`, `deploy/`.
- **Bản in:** giao diện hỏi đáp/citation; top-k hoặc vector metadata; cây source.

---

## Câu 10 — RAG: triển khai

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án gợi ý

- **Deployment view:** `Browser → Web/CDN → Query API pod → [Embedding API | LLM API | Pinecone]`; `Data sources → Crawler → Kafka/Temporal → Index Worker → Pinecone`; tất cả → OTel/Grafana.
- **Artifact/công cụ:** Web static bundle; Docker images cho Query API/Crawler/Worker; Kubernetes; Kafka/Temporal; managed Pinecone/LLM; Secret/ConfigMap.
- **Các bước:** tạo vector index đúng dimension → cấu hình namespace/ACL → lưu API keys trong Secret → build/push images → deploy queue/crawler/worker → index dữ liệu mẫu → kiểm tra vector/metadata → deploy Query API/Web → test câu biết/không biết đáp án và phân quyền → index toàn bộ.
- **Vận hành:** đặt timeout, retry, DLQ, probe, autoscaling, log/trace; rollback image hoặc rebuild index khi lỗi.
- **Bản in:** lệnh deploy; trạng thái containers/pods; Pinecone UI; log worker và giao diện query.

---

## Câu 11 — LLM-based Agent: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

### Đáp án gợi ý

- **Core:** agent lặp `quan sát trạng thái → LLM chọn hành động/tool → chạy tool → đọc kết quả` đến khi hoàn thành hoặc chạm giới hạn.
- **Logic view:** `User → Chat UI → Agent Orchestrator ↔ LLM`; `Orchestrator → Permission Check → Tool Registry → Tool Result`; Memory/Checkpoint/Audit nối với Orchestrator.
- **Công cụ:** React; LangGraph/custom Python; JSON Schema/Pydantic cho tool; PostgreSQL/Redis cho state; OpenTelemetry cho audit/trace; LLM API.
- **Đặc tính và kiểm tra:**
  - Correctness: bộ task có kết quả/tool sequence mong đợi; đo task success.
  - Safety/security: thử user thiếu quyền, prompt injection và write tool; policy phải chặn/đòi approval.
  - Bounded execution/cost: task tạo loop phải dừng ở `max_steps`, timeout hoặc budget.
  - Reliability: mock tool timeout/5xx; kiểm tra retry, checkpoint/resume và không lặp side effect.
  - Observability: mỗi model/tool call có trace, latency/token/cost và dữ liệu nhạy cảm đã che.
  - Modifiability: thêm Calculator theo cùng tool interface mà không sửa core loop.
- **Cây source:** `web/`, `agent/`, `tools/`, `policy/`, `storage/`, `tests/`, `deploy/`.
- **Bản in:** giao diện agent; cây source; một run/tool call thành công và thất bại.

---

## Câu 12 — LLM-based Agent: triển khai

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án gợi ý

- **Deployment view:** `Client → Gateway/Auth → Agent API → Temporal/Kafka → Agent Workers → [LLM | RAG | Tool Gateway → External APIs]`; Worker → Checkpoint DB, Secrets và OTel/Grafana.
- **Công cụ theo node:** Kong/Keycloak; FastAPI/Docker/Kubernetes; Temporal/Kafka; PostgreSQL; Vault/Kubernetes Secret; OpenTelemetry/Jaeger/Grafana.
- **Các bước:** định nghĩa tool schema/quyền → lưu secret → build/push API/Worker images → deploy DB và queue → deploy Gateway/API/Tool Gateway/Workers → cấu hình probe/autoscale → đặt max steps/timeout/retry/approval/cost limit → test staging bằng mock/read-only tools → canary → monitor và rollback nếu lỗi.
- **Bản in:** lệnh/status deploy; trạng thái worker; trace một agent run và giao diện công cụ trực tuyến nếu dùng.

---

## Câu 13 — Event Sourcing: chất lượng và logic

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

### Đáp án gợi ý

- **Core:** events bất biến là nguồn sự thật; trạng thái hiện tại được tính bằng cách áp dụng events theo thứ tự.
- **Logic view:** `UI → Command API → Aggregate/rules → Event Store → Projector → Read Model ← Query API ← UI`.
- **Công cụ:** React; FastAPI; EventStoreDB/PostgreSQL append-only; Python projector; PostgreSQL Read Model; pytest/Locust.
- **Ví dụ:** `score=0 → QuizAnswered(+10) → AnswerCorrected(-2) → score=8`.
- **Đặc tính và kiểm tra:**
  - Auditability: xem event có actor/time/type/payload; ứng dụng không được sửa/xóa.
  - Recoverability: xóa read model, replay và so count/state/hash trước-sau.
  - Extensibility: tạo projector/report mới từ event cũ.
  - Performance: đo append latency/throughput, query latency và projection lag.
  - Consistency: gửi duplicate; kiểm tra idempotency; concurrent command sai `expected_version` phải bị từ chối.
- **Luồng:** Command API nạp stream → Aggregate kiểm rule → append event với version → Projector cập nhật Read Model idempotently → Query API đọc model.
- **Cây source:** `command_api/`, `domain/`, `projections/`, `query_api/`, `migrations/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; event rows/EventStoreDB UI; cây source.

---

## Câu 14 — Event Sourcing: triển khai

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án gợi ý

- **Deployment view:** `Browser → Ingress → Command API pods → EventStoreDB + volume`; `EventStoreDB → Projector pods → PostgreSQL Read DB`; `Browser → Query API pods → Read DB`; tất cả → OTel/Grafana.
- **Công cụ:** Docker/Kubernetes; EventStoreDB/PostgreSQL; volume/backup; Kubernetes Secret; OpenTelemetry/Grafana/Jaeger.
- **Các bước:** deploy Event Store có TLS/auth/backup → tạo event schema/role → deploy Read DB và migration → deploy Command API, test append/version → deploy Projector, replay và chờ lag về 0 → deploy Query API/Ingress → chạy E2E command-event-projection-query → kiểm tra backup/log/metric → rollback service nếu lỗi, không sửa event.
- **Bản in:** lệnh deploy; trạng thái pod/container; Event Store UI; log và trạng thái projector.

---

## Câu 15 — Event Sourcing: tiến trình xuất danh sách

### Đề bài rút gọn

- Chọn một chức năng xuất danh sách cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output.
- **Nộp kèm:** giao diện xem danh sách.

### Đáp án gợi ý

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

### Đề bài rút gọn

- Vẽ **storage view**.
- Liệt kê công cụ dùng để cài đặt thiết kế lưu trữ.
- Trình bày các bước cài đặt thiết kế lưu trữ.
- Vẽ luồng dữ liệu từ trạng thái ban đầu đến trạng thái cuối cùng.
- Giải thích cách tái tạo trạng thái hiện tại từ các event đã lưu.
- Liệt kê công cụ dùng để tái tạo trạng thái.
- Trình bày các bước tái tạo trạng thái.

### Đáp án gợi ý

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

### Đề bài rút gọn

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

### Đáp án gợi ý

- **Core:** producer phát sự kiện đã xảy ra; broker giữ/chuyển event; các consumer độc lập đăng ký và xử lý.
- **Logic view:** `Upload UI → Document API → PostgreSQL + Outbox → Kafka → [Extractor | Audit | Notification]`; `Extractor → TextExtracted → Kafka → Indexer → Pinecone`.
- **Công cụ:** React; FastAPI/Node; PostgreSQL; Kafka/RabbitMQ; Python consumers; JSON Schema/Avro; OpenTelemetry/Grafana.
- **Đặc tính và kiểm tra:**
  - Loose coupling: thêm Audit Consumer mà producer source/build không đổi.
  - Scalability: tạo tải, đo events/s và lag; tăng partition + consumer rồi đo lại.
  - Availability/durability: tắt consumer, phát event, bật lại; broker vẫn giữ và xử lý tiếp.
  - Reliability: thử retry/backoff, outbox và DLQ khi lỗi.
  - Idempotency: gửi cùng `event_id` hai lần; kết quả chỉ đổi một lần.
  - Observability: lần theo toàn luồng bằng `correlation_id`; dashboard có lag/retry/DLQ.
- **Cây source:** `producer_api/`, `outbox_relay/`, `consumers/`, `contracts/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; broker/topic UI; cây source.

---

## Câu 18 — Event-Driven: triển khai

### Đề bài rút gọn

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

### Đáp án gợi ý

- **Deployment view:** `Client → Ingress → Producer API pods → PostgreSQL + Outbox → Relay → Kafka topics/DLQ → Consumer pods → Databases`; tất cả → OTel/Prometheus/Grafana.
- **Công cụ:** Docker/Kubernetes; Nginx/Ingress; PostgreSQL; Debezium/polling relay; Kafka/RabbitMQ; Pinecone; Secret; OpenTelemetry/Grafana.
- **Các bước:** deploy broker/topic/DLQ → cấu hình replication, retention, ACL → deploy result DB và consumers → deploy business DB/outbox relay → deploy producer API → gửi event test → kiểm tra từng consumer/result → monitor lag/retry/DLQ → tăng partition/consumer nếu cần → test rollback consumer độc lập.
- **Bản in:** lệnh deploy/scale; trạng thái containers/pods; Kafka UI; log và trạng thái consumers.

---

## Câu 19 — Event-Driven: tiến trình nhập dữ liệu

### Đề bài rút gọn

- Chọn một chức năng nhập dữ liệu cụ thể.
- Vẽ **process view** cho chức năng đó.
- Liệt kê và giải thích các công cụ kiểm tra tính hợp lệ của input.
- Trình bày từng bước kiểm tra input.
- Trình bày từng bước ghi dữ liệu khi input hợp lệ.

### Đáp án gợi ý

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

### Đề bài rút gọn

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- Trình bày các bước log event từ lúc phát sinh đến lúc được xử lý.
- Trình bày các bước trace toàn bộ hành trình của event.
- Trình bày cách monitor event và các thành phần xử lý.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện hiển thị kết quả.

### Đáp án gợi ý

- **Observability view:** `Producer --event headers→ Kafka → Consumers → OTel Collector → [Loki/ELK | Jaeger/Tempo | Prometheus] → Grafana/Alertmanager`.
- **ID cần truyền:** `event_id` nhận diện event; `correlation_id` nhóm một nghiệp vụ; `traceparent` nối trace context; đặt trong message header.
- **Công cụ:** OTel SDK; Kafka headers; OTel Collector; Loki/ELK; Jaeger/Tempo; Prometheus; Grafana/Alertmanager.
- **Các bước:** producer tạo IDs/span và log lúc ghi outbox/publish → consumer extract context và tạo process span → log nhận/thành công/retry/DLQ → thu event rate, duration, lag, retry, DLQ size → export qua Collector → tạo dashboard/alert.
- **Log fields:** time, service, topic, partition, offset, status, duration và các ID; không log token/payload nhạy cảm.
- **Kiểm tra:** phát một event → tìm mọi log/trace theo correlation ID → xem producer và từng consumer → tạo consumer lỗi → kiểm tra retry, DLQ và alert.
- **Bản in:** lệnh xem log; log có IDs; trace Jaeger; dashboard lag/retry/DLQ.

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

### Đáp án gợi ý

- **Lựa chọn:** đề cho chọn Lambda hoặc Kappa; chọn **Kappa** và trình bày nhất quán Kappa.
- **Core:** chỉ có một stream pipeline cho dữ liệu mới và việc tính lại; khi đổi logic thì replay durable event log.
- **Logic view:** `React/FastAPI → Kafka event log → Flink/Kafka Streams → PostgreSQL/ClickHouse Serving DB → Report API → Dashboard`; logic mới: `Kafka → Processor v2 → Serving DB v2`.
- **Công cụ:** Kafka; Flink/Kafka Streams; PostgreSQL/ClickHouse; FastAPI/React/Grafana; Prometheus/Locust.
- **Đặc tính và kiểm tra:**
  - Near real time: đo event-time → serving-time latency, throughput và lag.
  - Scalability: tăng Kafka partition và processor parallelism; chạy lại cùng tải.
  - Fault tolerance: kill/restart processor; resume từ checkpoint, không mất/trùng kết quả.
  - Replay/recovery: consumer group mới replay vào DB v2; so count/sum/hash.
  - Evolvability: chạy v1/v2 song song, so output rồi chuyển Report API.
  - Correctness: event biết trước, duplicate/out-of-order; kiểm aggregate/window cuối.
- **Khác Lambda:** Kappa không có batch layer riêng nên ít pipeline hơn; phải giữ event log đủ lâu để replay.
- **Cây source:** `producer/`, `contracts/`, `stream_processor/`, `report_api/`, `tests/`, `deploy/`.
- **Bản in:** giao diện nhập; Kafka UI; cây source; dashboard latency/lag.

---

## Câu 22 — Lambda hoặc Kappa: tiến trình xuất báo cáo

### Đề bài rút gọn

- Sử dụng cùng kiến trúc Lambda hoặc Kappa đã chọn.
- Chọn một chức năng xuất báo cáo thống kê cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output của báo cáo.
- **Nộp kèm:** giao diện báo cáo và giao diện hiển thị dữ liệu thô của báo cáo.

### Đáp án gợi ý

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

## Checklist trước khi thi

- Vẽ đúng loại view mà đề yêu cầu.
- Ghi trách nhiệm/công cụ cạnh từng box và giao thức/dữ liệu trên mũi tên.
- Với process view, nêu đủ input → xử lý → output → nhánh lỗi.
- Với quality attributes, nêu đủ đặc tính → công cụ → cách thử → metric/kết quả.
- Chuẩn bị đúng bản in được yêu cầu trong câu hỏi.
