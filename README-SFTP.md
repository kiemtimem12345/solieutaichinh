# SFTP an toàn thay cho FTP thường

## Kết quả nền tảng
- GitHub Actions đã xác nhận `195.35.62.53:65002` trả SSH banner `SSH-2.0-OpenSSH_9.9` (run 44314037153).
- Đây mới là kết nối dịch vụ công khai, **không phải bằng chứng đã đăng nhập thành công**.
- FTPS cổng 21 vẫn gặp lỗi certificate mismatch; không hạ cấp sang plain FTP tự động.

## Cấu hình Hostinger
1. Trang web → `solieutaichinh.online` → Bảng điều khiển → tìm **Truy cập SSH / SSH Access**. Nếu gói hosting cho phép, bật SSH.
2. Xem **SSH IP**, **SSH username**, **port**. Port thường là **65002**. Tránh sử dụng user FTP phụ `u154814653.githubdeploy` cho SFTP nếu Hostinger chỉ cho phép SSH user chính.
3. Khuyến nghị tạo SSH key chuyên dùng. Đưa **public key** vào Hostinger, **private key** chỉ đưa vào GitHub Secret `SFTP_PRIVATE_KEY`. Tuyệt đối không commit private key.
4. Lấy host public key/fingerprint SSH của máy chủ **từ nguồn đáng tin cậy của Hostinger** để kiểm tra, rồi cấu hình GitHub Secret `SFTP_KNOWN_HOSTS` với dòng định dạng `[195.35.62.53]:65002 ssh-ed25519 AAAA...`. Không lấy khóa bằng `ssh-keyscan` rồi tin ngay mà không đối chiếu fingerprint.
5. GitHub Secrets: `SFTP_USERNAME`, `SFTP_PRIVATE_KEY`, `SFTP_KNOWN_HOSTS`.
6. GitHub Actions Variable: `SFTP_DATA_DIR=/home/u154814653/domains/solieutaichinh.online/public_html/data` (dựa theo hPanel đã cung cấp; xác minh SSH path chính xác trước triển khai).
7. Mở GitHub Actions → **Verify Hostinger SFTP read-only** → **Run workflow**. Script không tải lên, không xóa dữ liệu.

## Giới hạn
- Tài khoản FTP phụ `u154814653.githubdeploy` bị giới hạn trong `public_html/data`, nhưng chưa chắc được quyền truy cập SSH/SFTP.
- SSH/SFTP của Hostinger thường sử dụng tài khoản SSH của hosting; quyền có thể rộng hơn FTP phụ. Giữ workflow ở chế độ chỉ đọc tới khi xác minh giới hạn và sao lưu.
- Khi xác minh PASS, có thể bổ sung workflow upload chỉ 41 JSON, không ghi đè giao diện.
- Không bật FTP thường để tự động chuyển mật khẩu qua mạng; đây là biện pháp cuối cùng chỉ nên dùng khi có sự chấp thuận riêng cho lần chạy, và vẫn cần đảm bảo website có giao diện gốc.
