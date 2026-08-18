# Kiến trúc phần mềm — core của đúng 22 câu

Mỗi câu chỉ học ba thứ:

1. **Core:** ý chính của kiến trúc.
2. **Vẽ:** sơ đồ tối giản.
3. **Nói:** giải thích các box và mũi tên theo thứ tự.

## Từ vựng tối thiểu cho người bắt đầu từ số 0

- **Client/Frontend:** giao diện người dùng nhìn thấy, ví dụ trang web.
- **Backend/Service:** chương trình phía máy chủ thực hiện một nhóm chức năng.
- **API:** “cửa giao tiếp” để hai chương trình gửi yêu cầu và kết quả cho nhau.
- **Database:** nơi lưu dữ liệu lâu dài.
- **Request/response:** client gửi yêu cầu; server xử lý rồi trả kết quả.
- **Event:** thông báo rằng một việc **đã xảy ra**, ví dụ `OrderCreated`.
- **Message broker:** trạm trung chuyển event, ví dụ Kafka hoặc RabbitMQ.
- **Worker:** chương trình chạy nền để xử lý công việc.
- **Container/Docker:** gói chương trình cùng môi trường cần để chạy.
- **Replica:** một bản sao đang chạy của service. Nhiều replica cùng chia tải.
- **Load balancer:** phân request cho các replica.
- **Latency:** một request mất bao lâu. **Throughput:** xử lý được bao nhiêu request trong một khoảng thời gian.
- **Deploy:** đưa phần mềm lên môi trường để người dùng có thể sử dụng.
- **Scale:** tăng khả năng phục vụ khi tải tăng, thường bằng cách thêm replica.
- **Log:** dòng ghi lại một việc đã xảy ra. **Trace:** toàn bộ hành trình của một request qua hệ thống.

## Các góc nhìn — nhớ một lần

- **Logic view:** hệ thống có những thành phần nào và mỗi thành phần làm gì.
- **Deployment view:** phần mềm chạy trên máy/container nào.
- **Process view:** dữ liệu đi qua hệ thống theo thứ tự nào.
- **Development view:** source code chia thành thư mục/module nào.
- **Storage view:** lưu những dữ liệu nào và chúng liên hệ ra sao.
- **Security view:** xác thực, phân quyền và mã hóa ở đâu.
- **Observability view:** thu log và trace ở đâu.

---

## 1. Microservices — chất lượng và deployment

**Microservices là gì?** Thay vì viết toàn bộ hệ thống thành một chương trình lớn, ta chia nó thành nhiều chương trình nhỏ theo chức năng. Ví dụ cửa hàng có Order Service lo đơn hàng và Payment Service lo thanh toán. Mỗi service chạy riêng và nói chuyện qua mạng.

**Core:** Mỗi service có thể phát triển, deploy và scale tương đối độc lập.

**Vẽ:** `User → Load Balancer → API Gateway → [Order Service | Payment Service] → Database`

**Chất lượng:**

- Scalability: tăng số instance của service bị tải cao.
- Availability: một instance chết, instance khác tiếp tục chạy.
- Modifiability: sửa một service ít ảnh hưởng service khác.
- Performance: đo latency và throughput.

**Kiểm tra:** JMeter/Locust tạo tải; tắt một instance; tăng replica rồi đo lại.

**Triển khai:** test → build Docker image → deploy bằng Docker Compose/Kubernetes → kiểm tra health.

**In:** kết quả load test và trạng thái containers/pods.

---

## 2. Microservices — logic, giao tiếp và process

**Core:** Logic view cho biết service nào làm gì; process view cho biết một use case chạy theo thứ tự nào.

**Vẽ logic:** `Web → Gateway → Order Service → Order DB`; `Order Service → Payment Service`

**Giao tiếp:**

- REST/gRPC khi cần câu trả lời ngay.
- Message broker khi xử lý nền.

**Vẽ process đặt hàng:**

`User → Order Service → lưu order → Payment Service → thanh toán → trả kết quả`

Input là thông tin đơn hàng; output là đơn hàng thành công hoặc thất bại.

**In:** request/response và cây source.

---

## 3. Microservices — security và scaling

**Core security:** chỉ người đúng danh tính và đúng quyền mới truy cập được dữ liệu.

**Vẽ:** `User --HTTPS/JWT→ Gateway --kiểm tra quyền→ Services → encrypted DB`

- Authentication: bạn là ai?
- Authorization: bạn được làm gì?
- TLS mã hóa dữ liệu khi truyền.
- Secret không để trong source code.

**Core scaling:** thêm instance để chia tải.

**Vẽ:** `Load Balancer → [Service 1 | Service 2 | Service 3]`

**Thực hiện:** load test → tăng replica → chạy lại → so latency/throughput.

**In:** cấu hình bảo mật đã che secret và lệnh scale.

---

## 4. Microservices — logging và tracing

**Core:** Log cho biết chuyện gì xảy ra trong một service; trace cho biết một request đi qua những service nào.

**Vẽ:**

`Gateway → Service A → Service B → OpenTelemetry → [Log system | Jaeger]`

- Mỗi request có một `trace_id`.
- Các service truyền cùng `trace_id` cho nhau.
- Log chứa thời gian, service, thao tác, trace ID và lỗi.
- Không log password/token.

**Công cụ:** OpenTelemetry, ELK/Loki, Jaeger, Grafana.

**Kiểm tra:** gửi request → tìm log theo trace ID → mở trace và xem toàn bộ đường đi.

**In:** log và giao diện trace.

---

## 5. Microservices — development và storage

**Core development:** mỗi service là một module/source folder độc lập.

```text
services/
├── order-service/
├── payment-service/
└── notification-service/
deploy/
tests/
```

**Ví dụ mở rộng:** thêm Notification Service nhận sự kiện `OrderCreated`; test và deploy riêng, không sửa Payment Service.

**Core storage:** mỗi service sở hữu dữ liệu của mình.

**Vẽ:** `Customer 1—N Order 1—N OrderItem`; Order Service sở hữu Order DB.

**Kiểm thử:** unit test service mới → integration test message → end-to-end test đặt hàng.

**In:** cây thư mục, lệnh test và sơ đồ dữ liệu.

---

## 6. Micro-Frontends — chất lượng, logic, kết hợp và giao tiếp

**Micro-Frontend là gì?** Đây là ý tưởng Microservices áp dụng cho giao diện web: chia một frontend lớn thành nhiều phần nhỏ. Ví dụ Product MFE hiển thị sản phẩm, Cart MFE hiển thị giỏ hàng. App Shell ghép các phần đó thành một trang hoàn chỉnh.

**Core:** Mỗi phần giao diện có thể được một nhóm phát triển và deploy riêng.

**Vẽ:** `App Shell → [Product MFE | Cart MFE | Account MFE] → Backend API`

- App Shell giữ layout và routing.
- Mỗi MFE phụ trách một vùng chức năng.
- Có thể kết hợp bằng Module Federation.
- Giao tiếp bằng props, callback hoặc event; tránh shared global state lớn.

**Chất lượng:** dễ thay đổi/deploy từng MFE, lỗi một MFE không làm hỏng toàn trang, tải trang vẫn nhanh.

**Kiểm tra:** Storybook, component test, Lighthouse, thử tắt một MFE để xem fallback.

**In:** từng MFE và trang đã kết hợp.

---

## 7. Micro-Frontends — deployment

**Core:** mỗi MFE được build và deploy riêng; browser tải chúng vào App Shell.

**Vẽ:**

`Product repo → CI → CDN/product.js`

`Cart repo → CI → CDN/cart.js`

`Browser → App Shell → tải product.js và cart.js`

**Các bước:** test → build từng MFE → upload CDN → cập nhật Shell → chạy E2E → rollback version nếu lỗi.

**Công cụ:** npm, CI/CD, CDN, Docker hoặc static hosting.

**In:** lệnh build/deploy và giao diện sau deploy.

---

## 8. JAMstack — chất lượng và logic

**JAMstack là gì?** JAM là **JavaScript, APIs, Markup**:

- **Markup:** HTML được tạo sẵn khi build, không đợi người dùng mở trang mới tạo.
- **JavaScript:** làm trang có tương tác.
- **APIs:** cung cấp dữ liệu động như đăng nhập hoặc bình luận.

File đã tạo sẵn được đặt trên **CDN**, tức nhiều máy chủ phân phối nội dung ở gần người dùng. Vì server chủ yếu chỉ gửi file có sẵn nên trang thường nhanh và dễ chịu tải.

**Core:** tạo HTML trước lúc build, phát file tĩnh từ CDN, và chỉ gọi API cho phần động.

**Ví dụ:** blog tĩnh.

**Vẽ:** `Content/Git → Static Site Generator → HTML/CSS/JS → CDN → Browser`; `Browser → API` nếu cần dữ liệu động.

**Chất lượng:** nhanh, dễ scale, availability cao, ít server public hơn, deploy đơn giản.

**Kiểm tra:** Lighthouse; load test CDN; sửa bài viết → build lại → kiểm tra nội dung mới.

**Công cụ:** Next.js/Astro, GitHub Actions, Netlify/Vercel/CDN.

**In:** giao diện, cây source và kết quả build.

---

## 9. RAG — chất lượng và logic

**RAG là gì?** RAG là **Retrieval-Augmented Generation**. LLM vốn không biết tài liệu riêng của ta. Vì vậy hệ thống tìm các đoạn tài liệu liên quan đến câu hỏi, đặt chúng vào prompt, rồi mới yêu cầu LLM trả lời.

**Embedding** biến một đoạn chữ thành dãy số biểu diễn ý nghĩa. **Vector database** lưu các dãy số này để tìm những đoạn có ý nghĩa gần với câu hỏi.

**Core:** tìm đúng các đoạn tài liệu liên quan rồi đưa chúng cho LLM để trả lời có căn cứ.

**Vẽ indexing:** `Documents → Chunking → Embedding → Vector DB`

**Vẽ query:** `Question → Retrieve top-k chunks → Prompt + chunks → LLM → Answer`

**Ví dụ:** hỏi đáp trên giáo trình.

**Chất lượng:** lấy đúng đoạn, trả lời đúng tài liệu, citation đúng, phản hồi nhanh, không lấy tài liệu người khác.

**Kiểm tra:** chuẩn bị câu hỏi có đáp án → xem top-k chunks → xem answer/citation → đo latency.

**Công cụ:** embedding model, Pinecone/FAISS, LLM, FastAPI.

**In:** giao diện hỏi đáp và cây source.

---

## 10. RAG — deployment

**Core:** tách phần indexing chạy nền khỏi phần query phục vụ người dùng.

**Vẽ:**

`Documents → Index Worker → Embedding API → Vector DB`

`Browser → Query API → Vector DB + LLM API`

**Các bước:** tạo vector index → cấu hình API keys → deploy worker → index dữ liệu mẫu → deploy query API → hỏi thử câu đã biết đáp án.

**Công cụ:** Docker, cloud hosting, Pinecone/FAISS, LLM API.

**In:** lệnh triển khai, vector DB và giao diện query.

---

## 11. LLM-based Agent — chất lượng và logic

**LLM-based Agent là gì?** Chatbot thường chỉ trả lời bằng văn bản. Agent còn có thể quyết định gọi một công cụ, đọc kết quả rồi làm bước tiếp theo. Tool có thể là calculator, tìm kiếm hoặc API.

**Core:** Agent lặp lại quá trình “xem tình trạng → chọn hành động/tool → nhận kết quả” cho đến khi hoàn thành mục tiêu hoặc phải dừng.

**Vẽ:** `User → Agent → LLM → chọn Tool → Tool Result → Agent → Answer`

**Ví dụ:** agent nhận câu hỏi toán, gọi Calculator rồi trả kết quả.

**Thành phần:** Agent orchestrator, LLM, tool registry, memory và permission check.

**Chất lượng:** hoàn thành đúng task, chỉ gọi tool được phép, không chạy vô hạn, theo dõi được tool calls, dễ thêm tool.

**Kiểm tra:** task có đáp án biết trước; tool lỗi/timeout; user không có quyền; đo latency và số tool calls.

**In:** giao diện agent và cây source.

---

## 12. LLM-based Agent — deployment

**Core:** Agent API nhận yêu cầu; worker chạy các bước và gọi LLM/tools.

**Vẽ:** `Client → Agent API → Agent Worker → [LLM | Tools]`; `Worker → State DB`; tất cả → logs/traces.

**Các bước:** cấu hình tool và permission → lưu secret → deploy API/worker → đặt max steps/timeout → test với tool giả → mở cho user.

**Công cụ:** Docker, queue/workflow engine, LLM API, database, observability tools.

**In:** trạng thái deploy và một agent run.

---

## 13. Event Sourcing — chất lượng và logic

**Event Sourcing là gì?** Cách lưu thông thường chỉ giữ trạng thái hiện tại, ví dụ số dư là 70. Event Sourcing giữ toàn bộ những việc đã dẫn đến trạng thái đó: nạp 100 rồi rút 30. Các event cũ không bị sửa; muốn biết trạng thái hiện tại thì áp dụng chúng theo thứ tự.

**Core:** chuỗi event là dữ liệu gốc; trạng thái hiện tại được tính lại từ chuỗi đó.

**Ví dụ tài khoản ngân hàng:**

`0 --MoneyDeposited(100)→ 100 --MoneyWithdrawn(30)→ 70`

**Vẽ:** `Command → Aggregate kiểm tra rule → Event Store → Projector → Read Model → Query`

**Chất lượng:** có lịch sử/audit, dựng lại trạng thái, tạo read model mới, không mất/trùng event.

**Kiểm tra:** gửi command → xem event → xóa read model → replay events → kết quả phải giống trước.

**Công cụ:** EventStoreDB hoặc PostgreSQL, projector, read database.

**In:** giao diện nhập, event rows và cây source.

---

## 14. Event Sourcing — deployment

**Core:** Command API ghi Event Store; Projector đọc events và cập nhật Read DB; Query API đọc Read DB.

**Vẽ:** `Command API → Event Store → Projector → Read DB ← Query API`

**Các bước:** deploy Event Store → deploy Command API → deploy Read DB/Projector → replay events → deploy Query API → kiểm tra dữ liệu.

**Công cụ:** Docker, EventStoreDB/PostgreSQL, API service.

**In:** lệnh deploy và giao diện Event Store.

---

## 15. Event Sourcing — process xuất danh sách

**Core:** danh sách được đọc từ Read Model đã tính sẵn, không replay mọi event cho mỗi request.

**Vẽ:**

`Event Store → Projector → Read Model`

`User → Query API → Read Model → List → User`

**Ví dụ:** danh sách giao dịch ngân hàng.

**Luồng:** nhận filter/page → kiểm tra quyền → query Read Model → tạo DTO → trả danh sách.

Input là user, filter và page. Output là danh sách cùng tổng số dòng.

**In:** giao diện danh sách.

---

## 16. Event Sourcing — storage, data flow và rebuild

**Core storage:** Event Store chứa `event_id`, `aggregate_id`, `type`, `version`, `payload`, `time`; checkpoint lưu vị trí projector đã đọc.

**Vẽ:** `Initial State + Event 1 + Event 2 + ... → Current State`

**Các bước rebuild:**

1. Bắt đầu từ state rỗng.
2. Đọc events theo đúng version.
3. Áp dụng lần lượt từng event.
4. Lưu kết quả vào Read Model mới.
5. So sánh kết quả rồi chuyển Query API sang model mới.

**Công cụ:** EventStoreDB/PostgreSQL và projector script.

**In:** events trước và Read Model sau replay.

---

## 17. Event-Driven — chất lượng và logic

**Event-Driven Architecture là gì?** Một thành phần thông báo rằng một việc đã xảy ra. Các thành phần quan tâm sẽ tự phản ứng. Ví dụ Order Service phát `OrderCreated`; Email Consumer gửi email và Inventory Consumer trừ tồn kho.

**Producer** tạo event, **broker** trung chuyển, **consumer** nhận và xử lý event.

**Core:** producer không gọi trực tiếp từng consumer, nên có thể thêm consumer mới mà ít sửa producer.

**Ví dụ:** `Order Service --OrderCreated→ Kafka → [Email Consumer | Inventory Consumer]`

**Chất lượng:** dễ thêm consumer, scale consumer, chịu lỗi tạm thời, xử lý event không trùng.

**Kiểm tra:** phát event → xem consumers; tắt consumer rồi bật lại; gửi duplicate; tạo tải và đo queue lag.

**Công cụ:** Kafka/RabbitMQ, service API, database, Grafana.

**In:** giao diện nhập, broker UI và cây source.

---

## 18. Event-Driven — deployment

**Core:** broker và từng producer/consumer chạy thành các process/container riêng.

**Vẽ:** `Client → Producer API → Kafka → [Consumer A | Consumer B] → Databases`

**Các bước:** deploy broker/topic → deploy consumers → deploy producer → gửi event test → kiểm tra kết quả → scale consumer nếu lag cao.

**Công cụ:** Docker/Kubernetes, Kafka/RabbitMQ, monitoring.

**In:** lệnh deploy, broker UI và trạng thái consumers.

---

## 19. Event-Driven — process nhập dữ liệu

**Core:** chỉ dữ liệu hợp lệ mới được lưu và tạo event.

**Vẽ:** `User → API → Validate → DB + Outbox → Broker → Consumer → Result DB`

**Kiểm tra đầu vào:** đúng schema, đủ field, đúng quyền và đúng business rule.

- Sai: trả `400/403`, không lưu.
- Đúng: lưu dữ liệu và outbox event trong cùng transaction, trả ID.
- Consumer nhận event, xử lý và lưu kết quả.
- Lỗi tạm thời thì retry; lỗi nhiều lần đưa vào DLQ.
- Dùng `event_id` để không xử lý duplicate hai lần.

**In:** input đúng/sai, event và dữ liệu đã lưu.

---

## 20. Event-Driven — logging và tracing

**Core:** theo dõi một event từ producer qua broker đến mọi consumer.

**Vẽ:** `Producer → Broker → Consumer`; cả ba → `OpenTelemetry → Logs/Jaeger/Grafana`.

- Mỗi event có `event_id` và `correlation_id`.
- Producer log khi publish.
- Consumer log khi nhận, xử lý, retry hoặc đưa vào DLQ.
- Metrics quan trọng: event rate, processing time, consumer lag, retry, DLQ size.

**Kiểm tra:** phát một event → tìm toàn bộ log/trace theo correlation ID.

**In:** log, trace và dashboard consumer lag.

---

## 21. Kappa — chất lượng và logic

**Kappa Architecture là gì?** Đây là kiến trúc xử lý một dòng dữ liệu liên tục:

- **Stream:** dòng event đến liên tục, ví dụ từng lượt click.
- **Event log:** Kafka lưu các event theo thứ tự trong một khoảng thời gian.
- **Stream processor:** đọc từng event và cập nhật kết quả, ví dụ cộng số click mỗi ngày.
- **Serving/Report DB:** lưu kết quả đã tính để giao diện đọc nhanh.
- **Replay:** đọc lại event cũ từ đầu để tính lại kết quả.

Kappa chỉ dùng một kiểu xử lý stream. Khi công thức thay đổi, ta chạy processor mới và cho nó replay event log để tạo bảng kết quả mới.

**Core:** một stream pipeline xử lý dữ liệu mới; muốn tính lại thì replay event log qua processor.

**Ví dụ:** đếm lượt click theo ngày.

**Vẽ:** `Click Events → Kafka Log → Stream Processor → Report DB → Dashboard`

Khi đổi logic: `Kafka Log → Processor v2 → Report DB v2`.

**Chất lượng:** gần real time, scale bằng partitions/processors, resume từ checkpoint, rebuild được bằng replay.

**Kiểm tra:** tạo events có kết quả biết trước → đo latency/lag → tắt và bật processor → replay vào DB mới → so kết quả.

**Công cụ:** Kafka, Flink/Kafka Streams, database, Grafana.

**In:** giao diện nhập, raw events và dashboard.

---

## 22. Kappa — process xuất báo cáo

**Core:** stream processor tính sẵn số liệu; Report API chỉ đọc kết quả.

**Vẽ:**

`Click Event → Kafka → Processor → Report DB`

`User → Report API → Report DB → Chart/Table`

**Luồng:** event đến → kiểm tra duplicate → cộng số liệu theo ngày → lưu kết quả/checkpoint → API nhận khoảng ngày → đọc DB → trả báo cáo.

Input báo cáo là user và khoảng ngày. Output là số click mỗi ngày cùng thời điểm cập nhật cuối.

Processor chết thì chạy lại từ checkpoint; khi đổi công thức thì replay log vào bảng mới.

**In:** giao diện báo cáo và dữ liệu thô của báo cáo.

---

## Cách học nhanh nhất

Với mỗi câu, che tài liệu và tự làm ba việc:

1. Nói được câu **Core**.
2. Vẽ lại đúng một dòng **Vẽ**.
3. Giải thích từng box và mũi tên trong 2–3 phút.

Không học thêm ngoài những gì mình đã viết trên A4.
