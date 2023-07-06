const form = document.querySelector("#signup-form");

//비밀번호 확인
const checkPassword = () => {
  const formData = new FormData(form);
  const password1 = formData.get("password");
  const password2 = formData.get("password2");
  if (password1 === password2) {
    return true;
  } else return false;
};

const div = document.querySelector("#info");

const handleSubmit = async (event) => {
  event.preventDefault();
  const formData = new FormData(form);
  //해쉬 함수로 변환
  const sha256Password = sha256(formData.get("password"));
  formData.set("password", sha256Password);

  //비밀번호 확인
  if (checkPassword()) {
    const res = await fetch("/signup", {
      method: "POST",
      body: formData,
    });
    const data = await res.json();
    //회원 가입 성공하면 login.html로 이동 23.07.05
    if (data === "200") {
      alert("회원 가입에  성공했습니다");
      window.location.pathname = "/login.html";
    }
  } else {
    const div = document.querySelector("#info");
    div.innerText = "비밀번호가 일치하지 않습니다.";
    div.style.color = "red";
    form.appendChild(div);
  }
};

form.addEventListener("submit", handleSubmit);
