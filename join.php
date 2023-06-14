<?php
// join.php
// 클라이언트로부터 전달받은 데이터
$username = $_POST['username'];
$password = $_POST['password'];
$email = $_POST['email'];

// 데이터베이스 연결 설정
$servername = 'localhost';
$dbname = 'kdt_ram';
$db_username = 'allowdb';
$db_password = 'uWLcLlg!d7.GjW(g';

try {
    // 데이터베이스 연결
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $db_username, $db_password);

    // 에러 출력 설정
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // 아이디와 이메일 중복 확인
    $stmt = $conn->prepare("SELECT * FROM users WHERE username = :username OR email = :email");
    $stmt->bindParam(':username', $username);
    $stmt->bindParam(':email', $email);
    $stmt->execute();

    $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

    if (count($result) > 0) {
        echo "<script>alert('이미 사용 중인 값입니다. 다른 값을 넣어 주십시요.');</script>";
        echo "<script>window.location.href = 'main.html';</script>";
    } else {
        // 사용자 정보를 데이터베이스에 삽입
        $stmt = $conn->prepare("INSERT INTO users (username, password, email) VALUES (:username, :password, :email)");
        $stmt->bindParam(':username', $username);
        $stmt->bindParam(':password', $password);
        $stmt->bindParam(':email', $email);
        $stmt->execute();

        // 성공 메시지 출력 후 리다이렉트
        echo "<script>alert('사용자 정보가 성공적으로 저장되었습니다.');</script>";
        echo "<script>window.location.href = 'main.html';</script>";
    }
} catch (PDOException $e) {
    // 오류 메시지 출력 후 리다이렉트
    echo "<script>alert('오류: " . $e->getMessage() . "');</script>";
    echo "<script>window.location.href = 'main.html';</script>";
}

// 데이터베이스 연결 해제
$conn = null;
?>

