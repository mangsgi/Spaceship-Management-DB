<!-- Pilot.svelte -->
<script>
  import { createEventDispatcher } from 'svelte';

  const dispatch = createEventDispatcher();

  function navigateHome() {
    dispatch('navigateHome');
  }
</script>

<style>
  /* 스타일링 추가 */
</style>

<div>
  <h1>파일럿 페이지</h1>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 파일럿 관련 내용 추가 -->
</div>
