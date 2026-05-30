from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime, timezone
import random
from app import db
from app.main import main
from app.models import User, Game, Shot
from sqlalchemy.orm import joinedload

SHOP_ITEMS = {
    'ball': [
        {'id': 'ball_classic', 'name': 'Klasik Top', 'emoji': '⚽', 'price': 0, 'desc': 'Geleneksel dikişli futbol topu.', 'class': ''},
        {'id': 'ball_gold', 'name': 'Altın Top', 'emoji': '⚽', 'price': 100, 'desc': 'Kraliyet sarısı 24 ayar parlaklık.', 'class': 'ball-gold'},
        {'id': 'ball_neon', 'name': 'Neon Mavi Top', 'emoji': '⚽', 'price': 250, 'desc': 'Siber dünyadan parlayan elektrik ışığı.', 'class': 'ball-neon'},
        {'id': 'ball_fire', 'name': 'Alev Topu', 'emoji': '☄️', 'price': 500, 'desc': 'Fizik kurallarını yakan alevli şutlar.', 'class': 'ball-fire'},
    ],
    'jersey': [
        {'id': 'jersey_fb', 'name': 'Fenerbahçe Forması', 'emoji': '👕', 'price': 0, 'desc': 'Efsanevi Sarı Lacivert çubuklu forma.', 'class': 'jersey-fb'},
        {'id': 'jersey_gs', 'name': 'Galatasaray Forması', 'emoji': '👕', 'price': 0, 'desc': 'Aslanların parçalı Sarı Kırmızı forması.', 'class': 'jersey-gs'},
        {'id': 'jersey_bjk', 'name': 'Beşiktaş Forması', 'emoji': '👕', 'price': 150, 'desc': 'Kara Kartalın asil Siyah-Beyaz forması.', 'class': 'jersey-bjk'},
        {'id': 'jersey_ts', 'name': 'Trabzonspor Forması', 'emoji': '👕', 'price': 150, 'desc': 'Karadeniz fırtınasının Bordo-Mavi forması.', 'class': 'jersey-ts'},
        {'id': 'jersey_rm', 'name': 'Real Madrid Forması', 'emoji': '👕', 'price': 300, 'desc': 'Galaktiklerin bembeyaz forması.', 'class': 'jersey-rm'},
        {'id': 'jersey_barca', 'name': 'Barcelona Forması', 'emoji': '👕', 'price': 350, 'desc': 'Blaugrana renkleriyle efsaneleşen forma.', 'class': 'jersey-barca'},
        {'id': 'jersey_turkey', 'name': 'Türkiye Forması', 'emoji': '👕', 'price': 500, 'desc': 'Şanlı kırmızı-beyaz ay-yıldızlı forma.', 'class': 'jersey-turkey'},
    ],
    'decor': [
        {'id': 'decor_classic', 'name': 'Klasik Ağ', 'emoji': '🥅', 'price': 0, 'desc': 'Standart beyaz stadyum ağı.', 'class': 'decor-classic'},
        {'id': 'decor_gold', 'name': 'Altın Ağ', 'emoji': '🥅', 'price': 200, 'desc': 'Altın renginde parıldayan stadyum ağı.', 'class': 'decor-gold'},
        {'id': 'decor_neon', 'name': 'Neon Ağ', 'emoji': '🥅', 'price': 400, 'desc': 'Renk değiştiren siber neon ağ.', 'class': 'decor-neon'},
        {'id': 'decor_spider', 'name': 'Örümcek Ağı', 'emoji': '🕸️', 'price': 600, 'desc': 'Kaleyi örümcek ağlarıyla kapatın.', 'class': 'decor-spider'},
    ],
    'glove': [
        {'id': 'glove_classic', 'name': 'Klasik Eldiven', 'emoji': '🧤', 'price': 0, 'desc': 'Standart yeşil kaleci eldiveni.', 'class': 'glove-classic'},
        {'id': 'glove_pink', 'name': 'Pembe Eldiven', 'emoji': '🧤', 'price': 150, 'desc': 'Göz alıcı neon pembe kaleci eldiveni.', 'class': 'glove-pink'},
        {'id': 'glove_cyber', 'name': 'Siber Eldiven', 'emoji': '🤖', 'price': 300, 'desc': 'Mavi neon ışıklı robotik kaleci eldiveni.', 'class': 'glove-cyber'},
        {'id': 'glove_fire', 'name': 'Alevli Eldiven', 'emoji': '🔥', 'price': 500, 'desc': 'Kor ateş gibi yanan alevli kaleci eldiveni.', 'class': 'glove-fire'},
    ]
}

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
        current_user.coins += 10
    else:
        active_game.total_score -= 5
        
    db.session.commit()
    
    return jsonify({
        'success': True,
        'is_goal': is_goal,
        'zone': zone,
        'new_score': active_game.total_score,
        'earned_coins': 10 if is_goal else 0,
        'total_coins': current_user.coins
    })

@main.route('/reset_game', methods=['POST'])
@login_required
def reset_game():
    today = datetime.now(timezone.utc).date()
    active_game = None
    for game in current_user.games:
        if game.played_at.date() == today:
            active_game = game
            break
            
    if active_game:
        for shot in list(active_game.shots):
            db.session.delete(shot)
        active_game.total_score = 0
        db.session.commit()
        return jsonify({'success': True, 'message': 'Oyun başarıyla sıfırlandı.'})
    else:
        active_game = Game(user_id=current_user.id)
        db.session.add(active_game)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Yeni oyun başlatıldı.'})

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

@main.route('/shop')
@login_required
def shop():
    unlocked = current_user.unlocked_items.split(',')
    categorized_items = {}
    for category, items in SHOP_ITEMS.items():
        categorized_items[category] = []
        for item in items:
            item_copy = item.copy()
            item_id = item['id']
            item_copy['is_unlocked'] = item_id in unlocked
            
            is_equipped = False
            if category == 'ball' and current_user.equipped_ball == item_id:
                is_equipped = True
            elif category == 'jersey' and current_user.equipped_jersey == item_id:
                is_equipped = True
            elif category == 'decor' and current_user.equipped_decor == item_id:
                is_equipped = True
            elif category == 'glove' and current_user.equipped_glove == item_id:
                is_equipped = True
                
            item_copy['is_equipped'] = is_equipped
            categorized_items[category].append(item_copy)
            
    return render_template(
        'main/shop.html',
        title='Market',
        items=categorized_items,
        coins=current_user.coins
    )

@main.route('/shop/buy', methods=['POST'])
@login_required
def buy_item():
    data = request.get_json()
    if not data or 'item_id' not in data:
        return jsonify({'success': False, 'message': 'Eşya seçilmedi'}), 400
        
    item_id = data['item_id']
    
    found_item = None
    item_category = None
    for cat, items in SHOP_ITEMS.items():
        for it in items:
            if it['id'] == item_id:
                found_item = it
                item_category = cat
                break
        if found_item:
            break
            
    if not found_item:
        return jsonify({'success': False, 'message': 'Geçersiz eşya'}), 404
        
    unlocked = current_user.unlocked_items.split(',')
    if item_id in unlocked:
        return jsonify({'success': False, 'message': 'Bu eşya zaten satın alınmış'}), 400
        
    if current_user.coins < found_item['price']:
        return jsonify({'success': False, 'message': 'Yetersiz bakiye'}), 400
        
    current_user.coins -= found_item['price']
    unlocked.append(item_id)
    current_user.unlocked_items = ','.join(unlocked)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{found_item["name"]} başarıyla satın alındı!',
        'new_coins': current_user.coins
    })

@main.route('/shop/equip', methods=['POST'])
@login_required
def equip_item():
    data = request.get_json()
    if not data or 'item_id' not in data:
        return jsonify({'success': False, 'message': 'Eşya seçilmedi'}), 400
        
    item_id = data['item_id']
    
    found_item = None
    item_category = None
    for cat, items in SHOP_ITEMS.items():
        for it in items:
            if it['id'] == item_id:
                found_item = it
                item_category = cat
                break
        if found_item:
            break
            
    if not found_item:
        return jsonify({'success': False, 'message': 'Geçersiz eşya'}), 404
        
    unlocked = current_user.unlocked_items.split(',')
    if item_id not in unlocked:
        return jsonify({'success': False, 'message': 'Bu eşyayı kuşanmak için önce satın almalısınız'}), 400
        
    if item_category == 'ball':
        current_user.equipped_ball = item_id
    elif item_category == 'jersey':
        current_user.equipped_jersey = item_id
    elif item_category == 'decor':
        current_user.equipped_decor = item_id
    elif item_category == 'glove':
        current_user.equipped_glove = item_id
        
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'{found_item["name"]} başarıyla kuşanıldı!',
        'category': item_category,
        'item_id': item_id
    })

@main.app_errorhandler(404)
def not_found_error(error):
    return render_template('404.html', title='Sayfa Bulunamadı'), 404

@main.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html', title='Sunucu Hatası'), 500
