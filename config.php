<?php
$host = "localhost"; // 데이터베이스 호스트
$username = 'allowdb'; // 데이터베이스 사용자 이름
$password = 'uWLcLlg!d7.GjW(g'; // 데이터베이스 비밀번호
$database = 'kdt_ram'; // 데이터베이스 이름

// MySQL 데이터베이스에 연결
$connection = mysqli_connect($host, $username, $password, $database);

// 연결 오류를 확인
if (mysqli_connect_errno()) {
    die("데이터베이스 연결 실패: " . mysqli_connect_error());
}
?>

