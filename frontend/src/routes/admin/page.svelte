<script>
  import { createEventDispatcher } from 'svelte';
  const dispatch = createEventDispatcher();

  function goHome() {
    dispatch('navigateHome');
  }
</script>

<style>
  .page {
    text-align: center;
    padding: 50px;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    cursor: pointer;
  }
</style>

<div class="page">
  <h2>페이지 4</h2>
  <p>페이지 4에 오신 것을 환영합니다!</p>
  <button on:click={goHome}>홈으로 이동</button>
</div>
