# Bộ bản in nộp kèm — 22 câu

File này chỉ dùng để chuẩn bị **bản in**, không phải đáp án học thuộc. In từ trước, ghi số câu thật lớn trên từng tập. Trong 10 phút viết A4 không được xem; sau đó có 2 phút chọn tập liên quan.

## Trạng thái

- **Đã có bằng chứng chạy thật:** câu 4 và 20.
- **Chỉ cần chuẩn bị trang câu lệnh:** câu 1, 2, 3, 5, 7, 10, 12, 14, 18.
- **Phải bổ sung ảnh UI/cây source của project tương ứng:** câu 6, 8, 9, 11, 13, 15, 17, 21, 22.
- **Đề không yêu cầu bản in riêng:** câu 16 và 19.

---

## Câu 1 — Kiểm tra chất lượng và triển khai Microservices

```bash
docker compose up --build -d
docker compose ps
curl http://localhost:8081/availability
# Ví dụ công cụ tạo tải; đề không bắt buộc in kết quả load test
wrk -t2 -c20 -d30s http://localhost:8081/availability
```

Nộp trang lệnh này và, nếu có, một ảnh giao diện/cửa sổ terminal của công cụ kiểm tra.

## Câu 2 — Cài đặt mã nguồn Microservices

```bash
git clone <repository-url>
cd <repository>
docker compose build
docker compose up -d
docker compose ps
```

## Câu 3 — Thiết lập và thực hiện scaling

```bash
docker compose up -d --scale reservation=3
docker compose ps
# Hoặc Kubernetes:
kubectl scale deployment reservation --replicas=3
kubectl get pods
```

## Câu 4 — Logging và tracing Microservices

```bash
cd observability-demo
docker compose up --build -d
curl http://localhost:8081/availability
docker compose logs --no-log-prefix gateway reservation
```

![Jaeger: Gateway gọi Reservation Service](observability-demo/screenshots/cau-04-jaeger-trace.png)

Trong ảnh: **2 services, 2 spans** — `gateway-service: GET /availability` gọi `reservation-service: availability.check`.

## Câu 5 — Cài đặt component/service mới

```bash
docker compose build loyalty
docker compose up -d loyalty
docker compose ps loyalty
docker compose logs loyalty
```

## Câu 6 — Micro-Frontends

Phải chèn và in:

1. Ảnh Account/Search/Report Micro-Frontend chạy riêng.
2. Ảnh App Shell đã ghép các Micro-Frontend.

## Câu 7 — Triển khai Micro-Frontends

```bash
npm ci
npm test
npm run build
npx vercel --prod
```

## Câu 8 — JAMstack

Phải chèn và in:

1. Ảnh giao diện website.
2. Cây mã nguồn tạo bằng `tree -L 2 -I 'node_modules|.git'`.

## Câu 9 — RAG

Phải chèn và in:

1. Ảnh giao diện hỏi–đáp RAG.
2. Cây mã nguồn tạo bằng `tree -L 2 -I '.venv|node_modules|.git'`.

## Câu 10 — Triển khai RAG

Chọn **một** trong hai: trang lệnh dưới đây hoặc ảnh giao diện công cụ triển khai.

```bash
docker compose up --build -d
docker compose ps
docker compose logs rag-api indexer
```

## Câu 11 — LLM-based Agent

Phải chèn và in:

1. Ảnh giao diện Agent thực hiện một task.
2. Cây mã nguồn tạo bằng `tree -L 2 -I '.venv|node_modules|.git'`.

## Câu 12 — Triển khai LLM-based Agent

Chọn **một** trong hai: trang lệnh dưới đây hoặc ảnh giao diện công cụ triển khai.

```bash
docker compose up --build -d
docker compose ps
docker compose logs agent-api agent-worker
```

## Câu 13 — Event Sourcing

Phải chèn và in:

1. Ảnh giao diện nhập dữ liệu/command.
2. Cây mã nguồn tạo bằng `tree -L 2 -I '.venv|node_modules|.git'`.

## Câu 14 — Triển khai Event Sourcing

Chọn **một** trong hai: trang lệnh dưới đây hoặc ảnh giao diện công cụ triển khai.

```bash
docker compose up --build -d
docker compose ps
docker compose logs command-api projector query-api
```

## Câu 15 — Danh sách Event Sourcing

Phải chèn và in ảnh giao diện một danh sách được đọc từ Read Model.

## Câu 16 — Lưu trữ và replay Event Sourcing

Đề không ghi yêu cầu nộp kèm bản in riêng.

## Câu 17 — Event-Driven

Phải chèn và in:

1. Ảnh giao diện nhập dữ liệu.
2. Cây mã nguồn tạo bằng `tree -L 2 -I '.venv|node_modules|.git'`.

## Câu 18 — Triển khai Event-Driven

Chọn **một** trong hai: trang lệnh dưới đây hoặc ảnh giao diện công cụ triển khai.

```bash
docker compose up --build -d
docker compose ps
docker compose logs producer consumer
```

## Câu 19 — Nhập dữ liệu Event-Driven

Đề không ghi yêu cầu nộp kèm bản in riêng.

## Câu 20 — Observability Event-Driven

```bash
cd observability-demo
docker compose up --build -d
curl -X POST http://localhost:8081/book \
  -H 'Content-Type: application/json' \
  -d '{"hotelId":"hotel-01","userId":"user-01"}'
docker compose logs --no-log-prefix gateway reservation consumer
docker compose ps
```

![Jaeger: event đi từ producer đến consumer](observability-demo/screenshots/cau-20-jaeger-trace.png)

Trong ảnh: **3 services, 3 spans** — `POST /book → reservation.create → notification.handle`.

![Dữ liệu event thô trong Redpanda](observability-demo/screenshots/cau-20-du-lieu-event-tho.png)

Trong ảnh: topic `reservation-events`, partition/offset và JSON có `eventId`.

## Câu 21 — Kappa

Phải chèn và in:

1. Ảnh giao diện nhập event.
2. Cây mã nguồn tạo bằng `tree -L 2 -I '.venv|node_modules|.git'`.

## Câu 22 — Báo cáo Kappa

Phải chèn và in:

1. Ảnh bảng/biểu đồ báo cáo.
2. Ảnh dữ liệu thô tạo ra đúng báo cáo đó.

