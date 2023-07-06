<form id="signup-form" action="/signup" method="POST">
  <div>회원가입</div>
  <div>
    <label for="id">아이디</label>
    <input type="text" name="id " id="id" required />
  </div>
  <div>
    <label for="password">비밀번호</label>
    <input type="password" name="password " id="password" required />
  </div>
  <div>
    <label for="password2">비밀번호 확인</label>
    <input type="password" name="password2 " id="password2" required />
  </div>
  <div>
    <label for="name">이름</label>
    <input type="text" name="name " id="name" required />
  </div>
  <div>
    <label for="email">이메일</label>
    <input type="email" name="email " id="email" required />
  </div>
  <div>
    <button type="submit">회원 가입 하기</button>
  </div>
  <div id="info" />
</form>
