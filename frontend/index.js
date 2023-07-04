const calcTime = (timestamp) => {
  //한국시간 utc+9
  const curTime = new Date().getTime() - 9 * 60 * 60 * 1000;
  const time = new Date(curTime - timestamp);
  const hour = time.getHours();
  const minute = time.getMinutes();
  const second = time.getSeconds();
  // >= 0 안할경우 undifined가 뜸
  if (hour > 0) return "${hour}시간 전 ";
  else if (minute > 0) return `${minute}분 전`;
  else if (second > 0) return `${second}초 전`;
  else return "방금 전";
};

//main.index를 javascript로 표현

const renderData = (data) => {
  const main = document.querySelector("main");
  //array를 reverse (반대로)
  data
    .sort((a, b) => a)
    .forEach(async (obj) => {
      const div = document.createElement("div");
      div.className = "items-list";

      const imgDiv = document.createElement("div");
      imgDiv.className = "items-list__img";
      //await을 쓸 경우 위에 화살표함수 있는곳에 다가 async 넣기
      const img = document.createElement("img");
      const res = await fetch(`/images/${obj.id}`);
      const blob = await res.blob();
      const url = URL.createObjectURL(blob); //url 생성
      img.src = url;

      const InfoDiv = document.createElement("div");
      InfoDiv.className = "items-list__info";

      const InfoTitleDiv = document.createElement("div");
      InfoTitleDiv.className = "items-list__info-title";
      InfoTitleDiv.innerText = obj.title;

      const infoMetaDiv = document.createElement("div");
      infoMetaDiv.className = "items-list__info-meta";
      infoMetaDiv.innerText = obj.place + " " + calcTime(obj.insetAt);

      const InfoPriceDiv = document.createElement("div");
      InfoPriceDiv.className = "items-list__info-price";
      InfoPriceDiv.innerText = obj.price;

      imgDiv.appendChild(img);
      InfoDiv.appendChild(InfoTitleDiv);
      InfoDiv.appendChild(infoMetaDiv);
      InfoDiv.appendChild(InfoPriceDiv);
      div.appendChild(imgDiv);
      div.appendChild(InfoDiv);
      main.appendChild(div); //data를 불러온 다음 div를 만들어서 그안 data에 div를 넣어서 실행
    });
}; //froe 각각의 어레이 내부에있는 항목을 돌면서 실행

const fetchList = async () => {
  const res = await fetch("/items");
  const data = await res.json();
  renderData(data);
};

fetchList();
