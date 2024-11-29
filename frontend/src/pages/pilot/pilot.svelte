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
  <h2>파일럿 페이지</h2>
  <p>파일럿 home에 오신 것을 환영합니다!</p>
  <button on:click={goHome}>홈으로 이동</button>

  <div class="button-container">
    <button on:click={() => handleButtonClick(1)}>PILOT</button>
    <button on:click={() => handleButtonClick(2)}>MECHANIC</button>
    <button on:click={() => handleButtonClick(3)}>CUSTOMER</button>
    <button on:click={() => handleButtonClick(4)}>ADMIN</button>
  </div>
</div>
