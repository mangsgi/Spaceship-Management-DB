
<script>
  import { navigate } from 'svelte-routing';
</script>

<style>
  @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400..900&family=Tinos:ital,wght@0,400;0,700;1,400;1,700&display=swap');

  .home {
  position: absolute; /* 또는 fixed */
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  
  text-align: center;
  padding: 0; /* 패딩 제거 */
  background-image: url('/images/space_main.png'); /* 원하는 배경 이미지 경로 */
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat; /* 배경 이미지 반복 방지 */
  background-attachment: fixed; /* 배경 이미지 고정 */
  color: white;
  width: 100vw; /* 전체 뷰포트 너비의 120% */
  height: 120vh; /* 전체 뷰포트 높이의 120% */
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  font-family: 'Orbitron', sans-serif;
  overflow: hidden; /* 필요에 따라 추가 */
}
  button {
    margin: 10px;
    padding: 15px 30px;
    font-family: 'Orbitron', sans-serif; /* 커스텀 글꼴 적용 */
    font-size: 1.2em;
    cursor: pointer;
    background-color: transparent; /* Button background transparent */
    border: 2px solid white; /* White border for the button */
    border-radius: 50px; /* Rounded edges for the button */
    color: white; /* Button text color */
    transition: background-color 0.3s, color 0.3s; /* Smooth transition for hover effects */
  }
  button:hover {
    background-color: white; /* Button background on hover */
    color: black; /* Text color on hover */
  }

  h1 {
    font-family: 'Tinos', sans-serif; /* 커스텀 글꼴 적용 */
    font-size: 5em; /* 필요에 따라 크기 조절 */
    margin-bottom: 20px;
  }

  .title {
    letter-spacing: 12px; /* 원하는 간격 설정 (2px은 예시) */
  }
</style>

<div class="home">
  <h1 class="title">Cosmic Odyssey</h1>
  <button on:click={() => navigate('/login')}>explore</button>
</div>
