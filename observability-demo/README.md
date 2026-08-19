# Demo dùng chung cho câu 4 và câu 20

Chạy hệ thống:

```bash
docker compose up --build -d
docker compose ps
```

Tạo một request/event:

```bash
curl -X POST http://localhost:8081/book \
  -H 'Content-Type: application/json' \
  -d '{"hotelId":"hotel-01","userId":"user-01"}'
```

Tạo request Microservices chỉ đi qua hai service (câu 4):

```bash
curl http://localhost:8081/availability
docker compose logs --no-log-prefix gateway reservation
```

Xem log có cùng `eventId`:

```bash
docker compose logs --no-log-prefix gateway reservation consumer
```

Giao diện:

- Jaeger: http://localhost:16686
- Redpanda Console: http://localhost:8080

Trong Jaeger, chọn service `gateway-service`, nhấn **Find Traces**, rồi mở trace
`POST /book`. Trace thể hiện request qua hai microservice và event được consumer xử lý.
