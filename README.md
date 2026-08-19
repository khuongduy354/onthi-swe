# 22 câu hỏi thi Kiến trúc phần mềm — bản viết lại ngắn gọn

- **Đề gốc:** [PDF 22 câu hỏi vấn đáp](materials/22-cau-hoi-thi-kien-truc-phan-mem.pdf) — GV. TS. Ngô Huy Biên, 2026.
- **Tài liệu chính:** [22 câu hỏi rút gọn kèm đáp án](22-CAU-HOI-VA-DAP-AN.md).
- **Cheat sheet nhớ nhanh:** [Core và quality attributes của 22 câu](CHEATSHEET-NHO-NHANH.md).
- **Bộ bản in:** [Bản in nộp kèm cho 22 câu](BAN-IN-NOP-KEM-22-CAU.md).
- **Demo chạy thật câu 4 và 20:** [Observability demo](observability-demo/README.md).
- Bản dưới đây chỉ **viết lại đề thi** thành các bullet ngắn gọn; không thêm nội dung trả lời.

## Yêu cầu chung

- Có **10 phút** viết câu trả lời trên giấy A4, không sử dụng tài liệu; sau đó có **2 phút** chọn bản in liên quan.
- Với khái niệm/phương pháp, trả lời ngắn gọn: **WHAT** (là gì), **HOW** (làm thế nào), **WHY** (lợi ích/khó khăn) và **WHEN** (khi nào áp dụng).
- Với **logic view**, ghi chức năng/trách nhiệm, quan hệ và công nghệ/ngôn ngữ của từng thành phần.
- Với **deployment view**, ghi node phần cứng/phần mềm, artifact/module chạy trên node và giao thức kết nối.
- Với **process view**, ghi input cụ thể, các bước biến đổi, output cụ thể và công nghệ thực hiện.
- Chỉ trình bày điều đã học/thực hành; không suy diễn không có bằng chứng.
- Nộp đúng bản in giao diện/câu lệnh mà câu hỏi yêu cầu; nên ghi số câu lên bản in để chọn nhanh.
- Trình bày to, rõ ràng, mạch lạc và giải thích được mọi box/mũi tên đã vẽ.
- Phần vấn đáp kéo dài khoảng **5–10 phút**; phải giải thích được nội dung đã viết và trả lời câu hỏi bổ sung.
- **Chấm điểm:** giấy A4 bỏ trống/không liên quan là 0; trả lời thiếu hoặc thiếu bản in tối đa 8; trả lời đủ kèm đúng bản in được trên 8–10 điểm.
- Được đổi phiếu tối đa 2 lần; mỗi lần đổi bị trừ 2 điểm.

---

## Câu 1 — Microservices: chất lượng và triển khai

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Liệt kê công cụ có thể dùng để kiểm tra các đặc tính đó.
- Trình bày các bước kiểm tra.
- Vẽ **deployment view**.
- Ghi công cụ triển khai cho từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** giao diện/câu lệnh kiểm tra chất lượng và câu lệnh triển khai.

## Câu 2 — Microservices: logic, giao tiếp và tiến trình

- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách các service giao tiếp với nhau.
- Vẽ **process view** cho một use case cụ thể.
- **Nộp kèm:** câu lệnh cài đặt mã nguồn hệ thống.

## Câu 3 — Microservices: bảo mật và mở rộng

- Vẽ **security view**.
- Ghi công cụ dùng để cài đặt bảo mật cho từng thành phần.
- Vẽ **scalability view**.
- Ghi công cụ dùng để mở rộng từng thành phần.
- **Nộp kèm:** câu lệnh thiết lập khả năng mở rộng và câu lệnh thực hiện scale hệ thống.

## Câu 4 — Microservices: logging và tracing

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện kết quả thu được.

## Câu 5 — Microservices: phát triển và lưu trữ

- Vẽ **development view**.
- Ghi mục đích của từng thư mục trên sơ đồ.
- Nêu một ví dụ thay đổi hoặc mở rộng hệ thống.
- Trình bày từng bước thay đổi, mở rộng và kiểm thử sao cho ít ảnh hưởng toàn bộ mã nguồn.
- Vẽ **storage view**.
- Ghi mục đích của từng thực thể lưu trữ.
- **Nộp kèm:** câu lệnh cài đặt thêm một thành phần mới.

## Câu 6 — Micro-Frontends: chất lượng, logic, kết hợp và giao tiếp

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- Giải thích cách kết hợp các giao diện thành hệ thống hoàn chỉnh.
- Giải thích cách các giao diện giao tiếp với nhau.
- **Nộp kèm:** giao diện từng Micro-Frontend và giao diện tổng hợp.

## Câu 7 — Micro-Frontends: triển khai

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh triển khai.

## Câu 8 — JAMstack: chất lượng và logic

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

## Câu 9 — RAG: chất lượng và logic

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

## Câu 10 — RAG: triển khai

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

## Câu 11 — LLM-based Agent: chất lượng và logic

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện hệ thống và cây thư mục mã nguồn.

## Câu 12 — LLM-based Agent: triển khai

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

## Câu 13 — Event Sourcing: chất lượng và logic

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

## Câu 14 — Event Sourcing: triển khai

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

## Câu 15 — Event Sourcing: tiến trình xuất danh sách

- Chọn một chức năng xuất danh sách cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output.
- **Nộp kèm:** giao diện xem danh sách.

## Câu 16 — Event Sourcing: lưu trữ và tái tạo trạng thái

- Vẽ **storage view**.
- Liệt kê công cụ dùng để cài đặt thiết kế lưu trữ.
- Trình bày các bước cài đặt thiết kế lưu trữ.
- Vẽ luồng dữ liệu từ trạng thái ban đầu đến trạng thái cuối cùng.
- Giải thích cách tái tạo trạng thái hiện tại từ các event đã lưu.
- Liệt kê công cụ dùng để tái tạo trạng thái.
- Trình bày các bước tái tạo trạng thái.

## Câu 17 — Event-Driven: chất lượng và logic

- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Giải thích cách kiểm tra từng đặc tính.
- Vẽ **logic view**.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

## Câu 18 — Event-Driven: triển khai

- Vẽ **deployment view**.
- Ghi công cụ triển khai từng thành phần trên sơ đồ.
- Trình bày các bước triển khai hệ thống.
- **Nộp kèm:** câu lệnh hoặc giao diện công cụ trực tuyến dùng để triển khai.

## Câu 19 — Event-Driven: tiến trình nhập dữ liệu

- Chọn một chức năng nhập dữ liệu cụ thể.
- Vẽ **process view** cho chức năng đó.
- Liệt kê và giải thích các công cụ kiểm tra tính hợp lệ của input.
- Trình bày từng bước kiểm tra input.
- Trình bày từng bước ghi dữ liệu khi input hợp lệ.

## Câu 20 — Event-Driven: logging, tracing và monitoring

- Vẽ **observability view** gồm logging và tracing.
- Ghi công cụ cài đặt từng thành phần giám sát trên sơ đồ.
- Trình bày các bước log event từ lúc phát sinh đến lúc được xử lý.
- Trình bày các bước trace toàn bộ hành trình của event.
- Trình bày cách monitor event và các thành phần xử lý.
- **Nộp kèm:** câu lệnh xem kết quả giám sát và giao diện hiển thị kết quả.

## Câu 21 — Lambda hoặc Kappa: chất lượng và logic

- Chọn **một** kiến trúc: Lambda hoặc Kappa.
- Liệt kê các đặc tính chất lượng mong muốn đạt được.
- Liệt kê công cụ dùng để kiểm tra các đặc tính đó.
- Trình bày các bước kiểm tra.
- Vẽ **logic view** của kiến trúc đã chọn.
- Ghi công cụ cài đặt từng thành phần trên sơ đồ.
- **Nộp kèm:** giao diện nhập dữ liệu và cây thư mục mã nguồn.

## Câu 22 — Lambda hoặc Kappa: tiến trình xuất báo cáo

- Sử dụng cùng kiến trúc Lambda hoặc Kappa đã chọn.
- Chọn một chức năng xuất báo cáo thống kê cụ thể.
- Vẽ **process view** cho chức năng đó.
- Thể hiện rõ input, các bước xử lý và output của báo cáo.
- **Nộp kèm:** giao diện báo cáo và giao diện hiển thị dữ liệu thô của báo cáo.
