<!-- routes/Home.svelte -->
<script>
  import { navigate } from 'svelte-routing';
</script>

<style>
  .home {
    text-align: center;
    padding: 50px;
  }
  button {
    margin: 10px;
    padding: 15px 30px;
    font-size: 1.2em;
    cursor: pointer;
  }
</style>

<div class="home">
  <h1>환영합니다!</h1>
  <button on:click={() => navigate('/login')}>로그인</button>
</div>
