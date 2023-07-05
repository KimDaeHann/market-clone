const form = document.getElementById("write-form");

const handleSubmitForm = async (event) => {
  event.preventDefault(); //try 안에서 로직시작해서 오류나면 catch를 함
  //세계시간 기준으로
  const body = new FormData(form);
  body.append("insertAt", new Date().getTime()); //body에 정보를 추가 append 컬럼명은 insetAt
  try {
    const res = await fetch("/items", {
      method: "POST",
      body: body, //body 지워도 가능함
    });
    const data = await res.json();
    if (data === "200") window.location.pathname = "/"; //pathname을 /로 변경
  } catch (e) {
    console.error(e);
  }
};

form.addEventListener("submit", handleSubmitForm);
