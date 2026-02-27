"""
Wine Tasting → Particle Effect  |  Flask 추론 서버
실행: python app.py
접속: http://localhost:5000
"""
from flask import Flask, request, jsonify, render_template
import joblib
import numpy as np
import os

app = Flask(__name__)

# ── 모델 로드 ────────────────────────────────────────────────
MODEL_DIR = os.path.join(os.path.dirname(__file__), 'models')

try:
    rf         = joblib.load(os.path.join(MODEL_DIR, 'rf_regressor.pkl'))
    rf_clf     = joblib.load(os.path.join(MODEL_DIR, 'rf_classifier.pkl'))
    scaler_cnt = joblib.load(os.path.join(MODEL_DIR, 'scaler_count.pkl'))
    print('✅ 모델 로드 완료')
except FileNotFoundError:
    print('❌ models/ 폴더를 찾을 수 없습니다.')
    print('   노트북을 실행하여 모델을 먼저 저장하세요.')
    rf = rf_clf = scaler_cnt = None

# ── Feature 컬럼 정의 (노트북과 동일한 순서) ──────────────────
FEATURE_COLS = [
    'is_red',
    'color_depth',
    'color_straw', 'color_lemon', 'color_gold', 'color_amber', 'color_brown',
    'color_purple', 'color_ruby', 'color_garnet',
    'nose_intensity',
    'fruit_green', 'fruit_citrus', 'fruit_stone', 'fruit_tropical',
    'fruit_red', 'fruit_black',
    'secondary_oak', 'secondary_creamy', 'tertiary_present',
    'development',
    'acidity', 'body', 'finish', 'tannin',
    'score_complexity', 'score_intensity',
]

PTYPE_NAMES = ['bubble', 'teardrop', 'smoke', 'shard', 'crystal']
PTYPE_DESC  = {
    'bubble':   '둥글고 가벼운 기포 형태',
    'teardrop': '눈물방울 — 부드럽고 흘러내리는',
    'smoke':    '퍼지는 연기 — 복잡하고 깊은',
    'shard':    '날카로운 파편 — 강렬하고 구조적',
    'crystal':  '결정 구조 — 섬세하고 정교한',
}


# ── 추론 함수 ────────────────────────────────────────────────
def predict_effect(raw: dict) -> dict:
    vec  = [float(raw.get(f, 0.0)) for f in FEATURE_COLS]
    X_in = np.array(vec).reshape(1, -1)

    pred  = rf.predict(X_in)[0]
    ptype = int(rf_clf.predict(X_in)[0])

    pcount_norm = float(np.clip(pred[2], 0, 1))
    pcount      = int(scaler_cnt.inverse_transform([[pcount_norm]])[0][0])

    name = PTYPE_NAMES[ptype]
    return {
        'particle_type':      ptype,
        'particle_type_name': name,
        'particle_type_desc': PTYPE_DESC[name],
        'particle_size':      round(float(np.clip(pred[1], 1.0, 5.0)), 3),
        'particle_count':     int(np.clip(pcount, 10, 300)),
        'particle_speed':     round(float(np.clip(pred[3], 0.0, 1.0)), 3),
        'gravity':            round(float(np.clip(pred[4], -1.0, 1.0)), 3),
        'color_r':            round(float(np.clip(pred[5], 0.0, 1.0)), 3),
        'color_g':            round(float(np.clip(pred[6], 0.0, 1.0)), 3),
        'color_b':            round(float(np.clip(pred[7], 0.0, 1.0)), 3),
    }


# ── 라우트 ───────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if rf is None:
        return jsonify({'error': '모델이 로드되지 않았습니다. 노트북을 먼저 실행하세요.'}), 503

    data = request.get_json(force=True)
    try:
        result = predict_effect(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
