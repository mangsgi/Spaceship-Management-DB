<script>
  import { Link, navigate } from 'svelte-routing';
  import { userId } from '../../stores.js'; // stores.js의 경로에 따라 조정

  function navigateHome() {
    navigate('/');
  }

  $: mechanicId = $userId;
</script>

<style>
  .mechanic-page {
    text-align: center;
    padding: 50px;
  }
  .mechanic-page button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  button {
    margin-top: 20px;
    padding: 10px 20px;
    cursor: pointer;
  }
</style>

<div class="mechanic-page">
  <h2>정비사 페이지</h2>
  <p>정비사 ID: {mechanicId}</p>
  <button on:click={navigateHome}>홈으로 돌아가기</button>
  <!-- 정비사 관련 내용 추가 -->

  <div>
    <h3>골라 들어가기</h3>
    <Link to="/mechanic/FindMyRepair">
      <button>본인 수리 조회</button>
    </Link>
    <Link to="/mechanic/?">
      <button>유지보수 기록 작성</button>
    </Link>
    <Link to="/mechanic/?">
      <button>수리할 우주선 상태 조회</button>
    </Link>
  </div>
</div>
