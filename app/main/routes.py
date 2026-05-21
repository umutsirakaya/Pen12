from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timezone
import random
from app import db
from app.main import main
from app.models import User, Game, Shot
from sqlalchemy.orm import joinedload

@main.route('/')
@main.route('/index')
def index():
    return render_template('index.html', title='Ana Sayfa')

@main.route('/play')
@login_required
def play():
    # Bugünkü aktif oyunu bul (UTC tarihine göre)
    today = datetime.now(timezone.utc).date()
    
    # Kullanıcının oyunlarını getir ve tarihleri karşılaştır (SQLite uyumluluğu için basit yöntem)
    active_game = None
    for game in current_user.games:
        if game.played_at.date() == today:
            active_game = game
            break
            
    if not active_game:
        # Bugün oyun yoksa yeni oluştur
        active_game = Game(user_id=current_user.id)
        db.session.add(active_game)
        db.session.commit()

    return render_template('main/game.html', title='Oyuna Başla', game=active_game)

@main.route('/shoot', methods=['POST'])
@login_required
def shoot():
    data = request.get_json()
    if not data or 'zone' not in data:
        return jsonify({'success': False, 'message': 'Bölge seçilmedi'}), 400
        
    zone = int(data['zone'])
    if not (1 <= zone <= 12):
        return jsonify({'success': False, 'message': 'Geçersiz bölge'}), 400

    today = datetime.now(timezone.utc).date()
    active_game = None
    for game in current_user.games:
        if game.played_at.date() == today:
            active_game = game
            break

    if not active_game:
         return jsonify({'success': False, 'message': 'Aktif oyun bulunamadı'}), 404

    # Olasılık Motoru
    hard_zones = [1, 3, 10, 12]
    medium_zones = [2, 4, 6, 7, 9, 11]
    easy_zones = [5, 8]
    
    if zone in hard_zones:
        prob = 0.60
    elif zone in medium_zones:
        prob = 0.75
    else:
        prob = 0.90
        
    # Şutun gol olup olmadığını belirle
    is_goal = random.random() < prob
    
    # Shot kaydı
    new_shot = Shot(game_id=active_game.id, target_zone=zone, probability=prob, is_goal=is_goal)
    db.session.add(new_shot)
    
    if is_goal:
        active_game.total_score += 1
    else:
        active_game.total_score -= 5
        
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_goal': is_goal,
        'zone': zone,
        'new_score': active_game.total_score
    })

@main.route('/leaderboard')
def leaderboard():
    # En yüksek skora sahip 10 oyunu kullanıcılarıyla birlikte çek
    # N+1 problemini engellemek için joinedload(Game.user) kullanıyoruz.
    top_games = db.session.execute(
        db.select(Game)
        .options(joinedload(Game.user))
        .order_by(Game.total_score.desc())
        .limit(10)
    ).scalars().all()
    
    return render_template('main/leaderboard.html', title='Liderlik Tablosu', top_games=top_games)

@main.route('/profile')
@login_required
def profile():
    # Kullanıcının tüm oyunlarını ve içindeki şutları (N+1 olmaksızın) çekiyoruz.
    # .unique() kullanılması önemli, çünkü join işlemleriyle tekrarlı satırlar gelebilir.
    games = db.session.execute(
        db.select(Game)
        .options(joinedload(Game.shots))
        .where(Game.user_id == current_user.id)
    ).unique().scalars().all()

    total_games = len(games)
    total_shots = 0
    total_goals = 0

    for game in games:
        total_shots += len(game.shots)
        total_goals += sum(1 for shot in game.shots if shot.is_goal)

    goal_ratio = 0
    if total_shots > 0:
        goal_ratio = round((total_goals / total_shots) * 100, 2)

    return render_template(
        'main/profile.html', 
        title='Profil',
        total_games=total_games,
        total_shots=total_shots,
        total_goals=total_goals,
        goal_ratio=goal_ratio
    )
