<?php
// 데이터베이스 연결 설정을 가져옴
require_once 'config.php';

// 클라이언트로부터 제공된 사용자 이름과 비밀번호 가져오기
$user = $_POST['username'];
$pass = $_POST['password'];

// 데이터베이스에서 사용자 이름과 비밀번호 검색
$query = "SELECT * FROM users WHERE username = '$user' AND password = '$pass'";
$result = mysqli_query($connection, $query);

// 쿼리 실행 결과를 확인
if ($result && mysqli_num_rows($result) > 0) {
    // 로그인 성공
    echo "로그인 성공!";
} else {
    // 로그인 실패
    echo "잘못된 사용자 이름 또는 비밀번호.";
}

// 데이터베이스 연결 종료
mysqli_close($connection);
?>

