<script>
  //모듈방식
  import Login from "./pages/Login.svelte";
  import NotFound from "./pages/NotFound.svelte";
  import Signup from "./pages/Signup.svelte";
  import Write from "./pages/Write.svelte";
  import Main from "./pages/main.svelte";
  import Router from "svelte-spa-router";
  import "./css/style.css";
  import { user$ } from "./store";
  import {
    GoogleAuthProvider,
    getAuth,
    signInWithCredential,
  } from "firebase/auth";
  import { onMount } from "svelte";

  let isLoading = true;

  const auth = getAuth();

  const checkLogin = async () => {
    const token = localStorage.getItem("token");
    if (!token) return (isLoading = false);

    const credential = GoogleAuthProvider.credential(null, token);
    const result = await signInWithCredential(auth, credential);
    const user = result.user;
    user$.set(user);
    isLoading = false;
  };

  const routes = {
    "/": Main,
    "/signup": Signup,
    "/write": Write,
    "*": NotFound,
  };

  onMount(() => checkLogin());
</script>

{#if isLoading}
  <div>로딩중입니다</div>
{:else if !$user$}
  <Login />
{:else}
  <Router {routes} />
{/if}
