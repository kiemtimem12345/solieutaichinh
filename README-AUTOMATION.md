# GitHub Actions → Hostinger: triển khai JSON có kiểm soát

Repository: kiemtimem12345/solieutaichinh; nhánh mặc định: main.

## Phạm vi
- Gói ZIP `so-lieu-hostinger-restore-2026-11-18-fixed.zip` được giữ nguyên làm nguồn lưu trữ; không thay thế, xóa hoặc sửa ZIP gốc.
- Kiểm tra 32 `financials-*.json` và 9 JSON phụ trợ, đúng tên mã, đúng cấu trúc và cú pháp JavaScript lưu trữ.
- Khi chuẩn bị xuất bản, lọc các kỳ BCTC **trước `2025-Q1`**, chỉ giữ **20 kỳ gần nhất** của từng mã; file JSON phụ trợ giữ nguyên. ZIP nguồn không thay đổi.
- Triển khai **chỉ 41 JSON đã chuẩn bị** vào thư mục data của website; không upload HTML, CSS, PHP, JavaScript hay dữ liệu provisional. Không xóa tệp trên máy chủ.
- Gói snapshot này **chưa có Q3/2026 đầy đủ cho 32 mã**; việc kiểm tra PASS là kiểm tra cấu trúc và phạm vi kỳ, không đồng nghĩa mọi số liệu tài chính đã xác minh đầy đủ.

## Cấu hình
1. GitHub Settings → Secrets and variables → Actions → Secrets: `FTP_SERVER`, `FTP_USERNAME`, `FTP_PASSWORD` (tuỳ chọn `FTP_PORT`; mặc định 21).
2. Actions → Variables: `FTP_DATA_DIR`: `/data/` nếu FTP đăng nhập trực tiếp tại `public_html`, hoặc `/public_html/data/` nếu FTP đăng nhập thư mục cha.
3. GitHub Settings → Environments: tạo `production`. Nếu có thể, thiết lập required reviewers.
4. Actions → **Validate financial snapshots** phải PASS.
5. **Chỉ sau khi khôi phục được giao diện website, sao lưu dữ liệu và xác minh root FTP**, vào Actions → **Deploy verified financial JSON to Hostinger** → Run workflow.

## Bảo vệ production
- Workflow triển khai mặc định chỉ chạy khi bấm thủ công, **không tự chạy khi push**.
- `scripts/deploy_ftp.py` chỉ dùng FTPS, có TLS kiểm tra chứng chỉ, không tự hạ cấp FTP không mã hóa.
- `FTP_DATA_DIR` chỉ cho phép `/data/` hoặc `/public_html/data/`.
- Script phải đọc được `CNAME` có chữ `solieutaichinh.online` trong thư mục cha từ phía FTP trước khi upload; nếu không sẽ dừng.
- Chỉ tải JSON, không có lệnh xóa file từ xa.
- Nếu dùng địa chỉ IP ở `FTP_SERVER` gây lỗi chứng chỉ FTPS, hãy sử dụng tên máy chủ FTPS do Hostinger cung cấp với chứng chỉ phù hợp. Không tắt kiểm tra TLS.
- Không gửi hoặc ghi mật khẩu FTP vào GitHub repository hay log workflow.

## Giới hạn chưa giải quyết
- Repo hiện chỉ có gói snapshot, README và workflow; chưa có `index.html`, CSS hoặc PHP gốc. Workflow upload JSON không thay thế được việc khôi phục giao diện.
- Tài khoản FTPS chưa được thử nghiệm từ GitHub Actions. Lần triển khai đầu tiên cần kiểm tra thực tế thủ công.
- Chỉ bật deploy tự động khi đã chạy thử thành công trên production.
