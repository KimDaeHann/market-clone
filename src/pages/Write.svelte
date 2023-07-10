<script>
  // @ts-nocheck

  import { getDatabase, ref, push } from "firebase/database";
  import Footer from "../components/Footer.svelte";
  import {
    getStorage,
    ref as refimage,
    uploadBytes,
    getDownloadURL,
  } from "firebase/storage";

  let title;
  let price;
  let description;
  let place;
  let files;

  const storage = getStorage();
  const db = getDatabase();

  async function writeUserData(imgurl) {
    push(ref(db, "items/"), {
      title,
      price,
      description,
      place,
      insertAt: new Date().getTime(),
      imgurl,
    });
    alert("글쓰기 완료");
    window.location.hash = "/";
  }

  const uploadFile = async () => {
    const file = files[0];
    const name = file.name;
    const imgRef = refimage(storage, name);
    await uploadBytes(imgRef, file);
    const url = await getDownloadURL(imgRef);
    return url;
  };

  const handleSubmit = async () => {
    const url = await uploadFile();
    writeUserData(url);
  };
</script>

<form id="write-form" on:submit|preventDefault={handleSubmit}>
  <div>
    <label for="image">이미지</label>
    <input type="file" bind:files id="image" name="image" />
  </div>
  <div>
    <label for="title">제목</label>
    <input type="text" id="title" name="title" bind:value={title} />
  </div>
  <div>
    <label for="text">가격</label>
    <input type="number" id="price" name="price" bind:value={price} />
  </div>
  <div>
    <label for="">설명</label>
    <input
      type="text"
      id="description"
      name="description"
      bind:value={description}
    />
  </div>
  <div>
    <label for="">장소</label>
    <input type="text" id="place" name="place" bind:value={place} />
  </div>
  <div>
    <button class="write-button" type="submit">글쓰기 완료!!</button>
  </div>
</form>

<Footer location="write" />

<style>
  .write-button {
    background-color: aqua;
    border-radius: 15px;
    margin: 10px 10px 0 10px;
    margin: 10px;
    color: black;
    padding: 5px 12px 5px 12px;
    cursor: pointer;
  }
</style>
