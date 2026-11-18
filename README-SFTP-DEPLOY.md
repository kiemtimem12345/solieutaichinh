# Quy trình upload JSON qua SFTP — chỉ chạy thủ công

## Trạng thái
- SSH Hostinger: `195.35.62.53:65002`, username `u154814653`.
- ED25519 fingerprint đã xác minh so với Hostinger hPanel: `SHA256:Wx4FFdj6dNVE5k+J6ubNerKOELb8xPqfPNVJ2ofhCHA`.
- Đây là workflow **chuẩn bị**, không tự động triển khai khi có commit. Không sử dụng FTP thường.
- Cần xác minh đăng nhập qua workflow read-only và khôi phục giao diện gốc (index.html / CSS / PHP) trước khi cho phép triển khai.

## Khi chuẩn bị xong
1. Bật SSH và thêm public key vào Hostinger; không gửi private key cho trợ lý.
2. GitHub Secrets: `SFTP_USERNAME=u154814653`, `SFTP_PRIVATE_KEY` là private key tương ứng với public key trong Hostinger.
3. GitHub Variable `SFTP_DATA_DIR=/home/u154814653/domains/solieutaichinh.online/public_html/data`.
4. Chạy Actions → `Verify Hostinger SFTP read-only` và yêu cầu PASS.
5. Khôi phục giao diện gốc, sao lưu website/dữ liệu và kiểm tra website hoạt động.
6. **Sau** các bước trên mới đặt GitHub Variable `SFTP_DEPLOY_ENABLED=YES_AFTER_UI_RESTORE`, tạo/kiểm tra environment `production`.
7. Chạy thủ công Actions → `Deploy validated JSON via SFTP (manual, guarded)`.

## An toàn
- Chỉ upload 41 JSON từ gói ZIP đã kiểm tra, lọc kỳ từ Q1/2025, tối đa 20 kỳ/mã.
- Dùng xác minh fingerprint ED25519 chính xác, không tắt strict host-key checking.
- Không xoá remote và không upload HTML/CSS/JS/PHP.
- Khóa `SFTP_DEPLOY_ENABLED` là biện pháp bảo vệ thao tác, không thay thế kiểm tra site production hay backup.
- Lưu ý tài khoản SSH chính có thể truy cập phạm vi rộng hơn tài khoản FTP phụ: **không ghi ngoài data**.
