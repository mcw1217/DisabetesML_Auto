# DiabetesML_Auto

* 머신러닝 기법을 사용하여 당뇨환자 데이터셋을 학습한 모델을 Flask로 제작한 웹서버에 올려 서비스를 만들어냈음 
* Flask 구현기능: 로그인,회원가입,세션, 관리자페이지, 유저페이지, 당뇨병 검사 및 병원 예약, 관리자페이지 예약 확인 및 삭제, 준지도학습

* 서비스: 병원예약 시스템을 통해 당뇨병 설문이 병원으로 전송되고, 병원의 진단 결과와 설문지를 서버로 보내 모델을 재학습 하는 준지도학습을 구현

## One Touch Install
start.exe를 실행하여, 자동으로 Miniconda설치와 Mysql 연동을 진행함 (Mysql은 아래 링크에서 다운로드 후 start.exe가 위치한 파일 넣어주고 start.exe를 실행시키면 자동으로 
설정이 완료됨

mysql 다운로드 링크
[https://drive.google.com/file/d/1tyE0_1dR1o6CFzuyeBVRuc5bABr3QX5p/view](https://drive.google.com/file/d/11xw8XUPPMWz_babnNe7B2qriffAxANgG/view?usp=sharing)

## Diabetes Dataset Analysis

Gender,Polyuria,Polydipsia,sudden weight loss,weakness,Polyphagia,Genital thrush,visual blurring,Itching,Irritability,delayed healing,partial paresis,muscle stiffness,Alopecia,Obesity,class

성별, 다뇨증, 다갈증(갈증을 느껴 수분섭취를 증가시키는 것), 체중감소, 약해짐, 다식증, 질효모감염증, 시각 흐려짐,가려움증, 과민성, 회복지연, 부분마비, 근육경직, 탈모증, 비만, 

https://ko.wikipedia.org/wiki/%EC%A7%88%ED%9A%A8%EB%AA%A8%EA%B0%90%EC%97%BC%EC%A6%9D
(질효모감염증) 질의 발적, 가려움, 통증, 흰색의 질 분비물 등의 증상이 있다.


## Model performance analysis


|        Model      |   Score Min   |   Score Mean   |   Cross Score Min   |   Cross Score Mean   |
|-------------------|---------------|----------------|---------------------|----------------------|
| Random Forest     | <b>train</b>: 1.0 <br><b>test</b>: 0.9134615384615 | <b>train</b>: 1.0 <br><b>test</b>: 0.9798461538461 | <b>train</b>: 0.9993975903614 <br><b>test</b>: 0.9496270797475 | <b>train</b>: 0.9999993975903 <br><b>test</b>: 0.9730432013769 |
| Gradient Boosting     | <b>train</b>: 0.9903846153846 <br><b>test</b>: 0.9134615384615 | <b>train</b>: 0.9980072115384 <br><b>test</b>: 0.9715576923076 | <b>train</b>: 0.9963963963963 <br><b>test</b>: 0.9374641422834 | <b>train</b>: 0.9994549314374 <br><b>test</b>: 0.9655523235800 |
| DecisionTreeClassifier     | <b>train</b>: 1.0 <br><b>test</b>: 0.9038461538461 | <b>train</b>: 1.0 <br><b>test</b>: 0.9205966724039 | <b>train</b>: 1.0<br><b>test</b>: 0.9205966724039 | <b>train</b>: 1.0  <br><b>test</b>: 0.9547946643717 |
| KneighborsClassifier     | <b>train</b>: 0.8990384615384 <br><b>test</b>: 0.7692307692307 | <b>train</b>: 0.9295600961538<br><b>test</b>: 0.8030407343660 | <b>train</b>: 0.8912207388111<br><b>test</b>: 0.8030407343660 | <b>train</b>: 0.915234163681  <br><b>test</b>: 0.8588829030407 |
| KneighborsClassifier     | <b>train</b>: 0.8990384615384 <br><b>test</b>: 0.7692307692307 | <b>train</b>: 0.9295600961538<br><b>test</b>: 0.8030407343660 | <b>train</b>: 0.8912207388111<br><b>test</b>: 0.8030407343660 | <b>train</b>: 0.915234163681  <br><b>test</b>: 0.8588829030407 |
| KneighborsClassifier_Plus     | <b>train</b>: 0.9350961538461 <br><b>test</b>: 0.8173076923076 | <b>train</b>: 0.9556682692307<br><b>test</b>: 0.9098942307692 | <b>train</b>: 0.9302923405333<br><b>test</b>: 0.8486230636833 | <b>train</b>: 0.9499196334889  <br><b>test</b>: 0.893440562248 |
| SVM    | <b>train</b>: 0.5865384615384 <br><b>test</b>: 0.5 | <b>train</b>: 0.6163245192307<br><b>test</b>: 0.6174326923076 | <b>train</b>: 0.5865389485871<br><b>test</b>: 0.5841652323580 | <b>train</b>: 0.6158167842541  <br><b>test</b>: 0.6153324440619 |


### Random Forest
최저점이 0.91을 넘고 테스트 평균 점수가 0.979로 그레이디언트 부스팅보다 약간 더 높다. 
crossvalidation score 평균은 0.973으로 그레이디언트 부스팅보다 0.008가량 더 높다.
단, 그레이디언트 부스팅보다 좀 더 학습하는데 시간이 걸린다.

### Gradient Boosting
최저점이 0.91을 넘고 테스트 평균 점수가 0.971을 넘는다. cross validation score 평균 역시 0.965를 넘는다
단, 학습시간이 다른 모델에 비해 3~4배 정도 더 걸린다.

### DecisionTreeClassifier
최저점이 0.9을 넘고 테스트 평균 점수가 0.96을 넘는다. cross validation score 평균 역시 0.95를 넘는다

### KneighborsClassifier
최저점이 낮고 테스트 평균 점수 여기 0.9를 넘지 못한다.


### KneighborsClassfier_Plus
파라미터인 n_neighbors의 값을 낮추어 진행) => 학습 1000회 수행 
기본 파라미터 값을 사용할때보다 성능이 나아짐

### SVM
매우 낮은 성능을 보임
