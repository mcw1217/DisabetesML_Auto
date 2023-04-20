<h1 style="text-align: center;">DisabetesML_Auto</h1>

* 머신러닝 기법을 사용하여 당뇨환자 데이터셋을 학습한 모델을 Flask로 제작한 웹서버에 올려 서비스를 만들어냈음 
* Flask 구현기능: 로그인,회원가입,세션, 관리자페이지, 유저페이지, 당뇨병 검사 및 병원 예약, 관리자페이지 예약 확인 및 삭제, 준지도학습

* 서비스: 병원예약 시스템을 통해 당뇨병 설문이 병원으로 전송되고, 병원의 진단 결과와 설문지를 서버로 보내 모델을 재학습 하는 준지도학습을 구현


*당뇨병 데이터셋 분석

Gender,Polyuria,Polydipsia,sudden weight loss,weakness,Polyphagia,Genital thrush,visual blurring,Itching,Irritability,delayed healing,partial paresis,muscle stiffness,Alopecia,Obesity,class

성별, 다뇨증, 다갈증(갈증을 느껴 수분섭취를 증가시키는 것), 체중감소, 약해짐, 다식증, 질효모감염증, 시각 흐려짐,가려움증, 과민성, 회복지연, 부분마비, 근육경직, 탈모증, 비만, 

https://ko.wikipedia.org/wiki/%EC%A7%88%ED%9A%A8%EB%AA%A8%EA%B0%90%EC%97%BC%EC%A6%9D
(질효모감염증) 질의 발적, 가려움, 통증, 흰색의 질 분비물 등의 증상이 있다.
