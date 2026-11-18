# GitHub Actions → Hostinger: triển khai JSON có kiểm soát

Repository: kiemtimem12345/solieutaichinh; nhánh mặc định: main.

## Phạm vi
- Lưu trữ dữ liệu đã kiểm tra trong gói `so-lieu-hostinger-restore-2026-11-18-fixed.zip` hiện có trên GitHub.
- Validate: 32 `financials-*.json` + 9 JSON phụ trợ, giải mã JSON và kiểm tra cú pháp JavaScript lưu trữ.
- Deploy: **chỉ 41 JSON** từ gói, vào thư mục data của website; không upload `assets/app.js`, `index.html`, CSS hoặc PHP và không xóa file đang tồn tại.
- File JS trong ZIP là bản lưu trữ cũ có tham chiếu GitHub cũ; không dùng để triển khai website.

## Cấu hình
1. GitHub Settings → Secrets and variables → Actions → Secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` (tuỳ chọn `FTP_PORT`; mặc định 21).
2. Actions → Variables: `FTP_DATA_DIR`, đúng bằng `/data/` nếu FTP đăng nhập trực tiếp tại `public_html`, hoặc `/public_html/data/` nếu FTP đăng nhập ở thư mục cha.
3. GitHub Settings → Environments: tạo `production`. Nếu có thể, thiết lập required reviewers.
4. Mở Actions → **Validate financial snapshots** để xem trạng thái PASS.
5. Chỉ khi website đã được khôi phục giao diện, FTP root được xác minh và đã sao lưu dữ liệu, vào Actions → **Deploy verified financial JSON to Hostinger** → Run workflow.

## Biện pháp bảo vệ
- Workflow triển khai chạy thủ công, **không tự triển khai khi push** cho đến khi có kiểm tra production thành công.
- `scripts/deploy_ftp.py` chỉ dùng FTPS (TLS kiểm tra chứng chỉ), không tự hạ cấp FTP thường.
- Bắt buộc `FTP_DATA_DIR` là `/data/` hoặc `/public_html/data/`.
- Trước khi tạo / tải lên `data`, script phải đọc được `CNAME` có chữ `solieutaichinh.online` ở thư mục cha. Nếu không thì dừng.
- Chỉ tải lên các file `*.json` được kiểm tra; không có lệnh xoá file trên máy chủ.
- Nếu FTPS báo lỗi chứng chỉ do `FTP_SERVER` là địa chỉ IP, dùng **tên máy chủ FTPS chính thức** có chứng chỉ TLS khớp từ Hostinger. Không tắt kiểm tra chứng chỉ để né lỗi.
- Bí mật FTP không đặt trong Git hoặc ghi vào log.

## Website hiện tại chưa đủ giao diện
Repository `main` tại thời điểm thiết lập chỉ có các file hồi phục và ZIP, không chứa giao diện gốc. Hoàn thành quy trình upload JSON **không** đồng nghĩa website sẽ được khôi phục. Cần đưa mã nguồn HTML/CSS/PHP gốc trở lại trước khi chạy triển khai.

Để bật tự động deploy ở giai đoạn sau, thay `workflow_dispatch` bằng thêm `push: branches: [main]` sau khi đã chạy thử thành công.
