<script>
  import "./app.css";
  import Router from "svelte-spa-router";
  import Home from "./pages/Home.svelte";
</script>

<Router routes={{
    "/": Home,
}} />