# WinaryXR — Wine Tasting → Particle Effect

와인 테이스팅 특성을 입력하면 AI(Random Forest)가 XR 파티클 이펙트 파라미터를 추론해주는 웹 앱입니다.
브라우저에서 테이스팅 시트를 체크하고 버튼을 누르면, Unity/XR에서 바로 사용할 수 있는 JSON 파라미터가 출력됩니다.

---

## 시작하기

### 1. conda 환경 만들기

```bash
conda create -n winaryxr python=3.11
conda activate winaryxr
```

### 2. 패키지 설치

```bash
pip install scikit-learn numpy pandas matplotlib seaborn flask joblib notebook
```

### 3. 모델 학습 및 저장

Jupyter Notebook을 열고 모든 셀을 실행합니다.

```bash
jupyter notebook wine_tasting_ml.ipynb
```

> 실행 완료 후 `models/` 폴더에 `.pkl` 파일 3개가 생성되어야 합니다.
> ```
> models/
>   rf_regressor.pkl
>   rf_classifier.pkl
>   scaler_count.pkl
> ```

### 4. Flask 서버 실행

```bash
python app.py
```

### 5. 브라우저에서 열기

```
http://localhost:5000
```

---

## 출력 파라미터 (Output)

| 파라미터 | 설명 |
|---|---|
| `particle_type` | 파티클 형태 (0=bubble / 1=teardrop / 2=smoke / 3=shard / 4=crystal) |
| `particle_size` | 파티클 크기 (1.0 ~ 5.0) |
| `particle_count` | 파티클 수 (10 ~ 300) |
| `particle_speed` | 이동 속도 (0.0 ~ 1.0) |
| `gravity` | 중력 방향 (−1.0 위 ↑ / +1.0 아래 ↓) |
| `color_r/g/b` | 파티클 색상 (0.0 ~ 1.0) |

---

## 파일 구조

```
WinaryXR Test/
├── wine_tasting_dataset.csv   # 학습 데이터
├── wine_tasting_ml.ipynb      # 모델 학습 노트북
├── app.py                     # Flask 서버
├── templates/
│   └── index.html             # 테이스팅 UI
└── models/                    # 학습 후 자동 생성
    ├── rf_regressor.pkl
    ├── rf_classifier.pkl
    └── scaler_count.pkl
```
