<script>
    // FindPilotFlight 페이지에 필요한 로직 추가
  import { userId } from '../../../stores.js'; // stores.js의 경로에 따라 조정

    // 반응형 선언으로 userId 값이 변경될 때마다 pilotId 업데이트
    $: pilotId = $userId;
</script>
  
<style>
  .page {
    text-align: center;
    padding: 50px;
  }
  button {
    margin: 5px;
    padding: 10px 20px;
    cursor: pointer;
    font-size: 1em;
  }
  input {
    margin: 5px;
    padding: 5px;
    font-size: 1em;
  }
  .error {
    color: red;
  }
  .loading {
    font-style: italic;
  }
</style>
  
  <div class="page">
    <h2>파일럿 비행 찾기</h2>
    <p>파일럿 ID: {pilotId}</p>
    <!-- 하위 페이지 내용 추가 -->
  </div>
  