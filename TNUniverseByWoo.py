import pygame, random


# !!!pygame에서 왼쪽 상단 끝이 0,0 이고 '아래'로 [y축(+)] '오른쪽'으로 [x축(+)]임!
# 벤치마킹 및 코드 레퍼런스 -> 파이썬 총알피하기

# pygame 라이브러리 사용을 위한 초기화 작업
pygame.init()

# 게임 끌 때 쓸 변수
endgame = False

# 게임 타이틀 및 화면 틀 생성
pygame.display.set_caption("TN Universe By Woo")
screen_width = 600
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# 게임 내 글자 폰트(기본글자 사용)
game_font = pygame.font.SysFont("arial", 20)

# 게임 배경화면 및 아이콘 -> 이미지 사이즈를 창 사이즈에 맞게 조정하기!
background = pygame.image.load("img\\universe.png")
icon = pygame.image.load("img\\DurianIcon.png")
pygame.display.set_icon(icon)

# FPS 설정을 통한 최적화를 위한 객체
time = pygame.time.Clock()


# 캐릭터(이하 두리안) 생성 및 정의 과정
durian = pygame.image.load("img\\Durian.png")
durian_size = durian.get_rect().size    # 이미지 사이즈 그대로 가져옴 -> 캐릭터 크기로 반영됨
durian_width = durian_size[0]   # 캐릭터의 가로길이
durian_height = durian_size[1]  # 캐릭터의 세로길이
durian_x_pos = (screen_width/2) - (durian_width/2)  # 캐릭터의 x좌표 (캐릭터 중심기준)
durian_y_pos = (screen_height/2) - (durian_height/2)    # 캐릭터의 y좌표 (캐릭터 중심기준)
durian_speed = 0.3  # 캐릭터의 이동 속도

# KeyDown시 이동에 필요한 변화값 -> 0 이면 멈춤
player_to_x = 0
player_to_y = 0

# 폭발 이미지
boom = pygame.image.load("img\\Boom.png")

# Enemy의 객체 및 기능을 정의하기 위해 클래스 활용
class Enemy:
    # Enemy 객체는 두리안 설정 때와 거의 동일함
    enemy_image = pygame.image.load("img\\Enemy.png")
    enemy_size = enemy_image.get_rect().size
    enemy_width = enemy_size[0]
    enemy_height = enemy_size[1]
    enemy_spawnPoint = None
    enemy_speed = 0
    enemy_x_pos = 0
    enemy_y_pos = 0
    enemy_rad = 0   # Enemy 방향 -> 움직일 각을 정함(리스트 안의 튜플 형태(기울기)로 표현해줄 것임)

    # 객체 구현화 작업
    enemy_rect = enemy_image.get_rect()
    enemy_rect.left = enemy_x_pos
    enemy_rect.top = enemy_y_pos

    # 난이도 옵션 적용
    def __init__(self, select):
        if select == 1:
            self.enemy_speed = random.choice([0.5, 0.75, 1.0, 1.25, 1.5])
        elif select == 2:
            self.enemy_speed = random.choice([0.5, 0.9, 1.3, 1.7, 2.1])
        elif select == 3:
            self.enemy_speed = random.choice([0.7, 1.3, 1.8, 2.3, 2.8])
            
        self.enemy_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

        # Enamy 등장 방향(각 화면 끝에서 스폰됨) -> 각 Side 별 생성 위치 및 이동방향 정의
        if self.enemy_spawnPoint == 'LEFT':
            self.enemy_x_pos = - self.enemy_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice([(1,3), (1,2), (2,2), (2,0), (2,1), (3,1), (2,-2), (1,-2), (1,-3), (2,-1), (3,-1)])
        elif self.enemy_spawnPoint == 'RIGHT':
            self.enemy_x_pos = screen_width
            self.enemy_y_pos = random.randint(0, screen_height - self.enemy_height)
            self.enemy_rad = random.choice([(-1,3), (-1,2), (-2,2), (-2,0), (-2,1), (-3,1), (-2,-2), (-1,-2), (-1,-3), (-2,-1), (-3,-1)])
        elif self.enemy_spawnPoint == 'UP':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = - self.enemy_height
            self.enemy_rad = random.choice([(3,1), (2,1), (2,2), (1,2), (1,3), (0,2), (-2,2), (-1,2), (-1,3), (-2,1), (-3,1)])
        elif self.enemy_spawnPoint == 'DOWN':
            self.enemy_x_pos = random.randint(0, screen_width - self.enemy_width)
            self.enemy_y_pos = screen_height
            self.enemy_rad = random.choice([(3,-1), (2,-1), (2,-2), (1,-2), (1,-3), (0,-2), (-1,-3), (-1,-2), (-2,-2), (-2,-1), (-3,-1)])

    # Enemy 이동 기능
    def enemy_move(self):
        self.enemy_x_pos += self.enemy_speed * self.enemy_rad[0]    # rad에 정의한 기울기의 x좌표값*속도만큼 이동
        self.enemy_y_pos += self.enemy_speed * self.enemy_rad[1]    # rad에 정의한 기울기의 y좌표값*속도만큼 이동
        global result
        
        # 위쪽 화면끝에 다다랐을 때
        def reach_up():
            if self.enemy_y_pos < -self.enemy_height:
                return True
        
        # 아래쪽 화면끝에 다다랐을 때
        def reach_down():
            if self.enemy_y_pos > screen_height:
                return True
        
        # 왼쪽 화면끝에 다다랐을 때
        def reach_left():
            if self.enemy_x_pos < -self.enemy_width:
                return True
        
        # 오른쪽 화면끝에 다다랐을 때
        def reach_right():
            if self.enemy_x_pos > screen_width:
                return True

        # 위에서 출발한 경우 "오른쪽/왼쪽/아래"에 다다라면 사라짐 + (점수+1)
        if self.enemy_spawnPoint == 'UP':
            if reach_left() or reach_right() or reach_down():
                enemy_list.remove(self)
                result += 1

        # 아래에서 출발한 경우 "오른쪽/왼쪽/위"에 다다라면 사라짐 + (점수+1)
        if self.enemy_spawnPoint == 'DOWN':
            if reach_left() or reach_right() or reach_up():
                enemy_list.remove(self)
                result += 1

        # 왼쪽에서 출발한 경우 "오른쪽/위/아래"에 다다라면 사라짐 + (점수+1)
        if self.enemy_spawnPoint == 'LEFT':
            if reach_up() or reach_down() or reach_right():
                enemy_list.remove(self)
                result += 1

        # 오른쪽에서 출발한 경우 "왼쪽/위/아래"에 다다라면 사라짐 + (점수+1)
        if self.enemy_spawnPoint == 'RIGHT':
            if reach_up() or reach_down() or reach_left():
                enemy_list.remove(self)
                result += 1

    # 충돌 시 객체 구현화 작업(충돌 판정을 좀 더 정확하게 하기 위해 재탕)
    def enemy_bump(self):
        self.enemy_rect = self.enemy_image.get_rect()
        self.enemy_rect.left = self.enemy_x_pos
        self.enemy_rect.top = self.enemy_y_pos


# Heart(보너스 점수) 정의 -> 기능적인 부분 Enemy와 거의 비슷
class Heart:
    heart_image = pygame.image.load("img\\Heart.png")
    heart_size = heart_image.get_rect().size
    heart_width = heart_size[0]
    heart_height = heart_size[1]
    heart_spawnPoint = None
    heart_speed = 0
    heart_x_pos = 0
    heart_y_pos = 0
    heart_rad = 0
    
    rainbow_check = False   # RainbowHeart의 기능 활용을 위한 변수

    heart_rect = heart_image.get_rect()
    heart_rect.left = heart_x_pos
    heart_rect.top = heart_y_pos

    def __init__(self, select):
        self.heart_spawnPoint = random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])
        
        # RainbowHeart 가 나올 수 있게 설정 -> 현재 10%
        heart_unique = random.randint(0,100)
        if heart_unique < 10:
            self.heart_image = pygame.image.load("img\\RainbowHeart.png")
            self.rainbow_check = True
            
        if self.rainbow_check:
            self.heart_speed = random.choice([1.5, 2.0, 2.5, 3.0])
        else:
            if select == 1:
                self.heart_speed = random.choice([0.5, 0.75, 1.0, 1.25, 1.5])
            elif select == 2:
                self.heart_speed = random.choice([0.5, 0.9, 1.3, 1.7, 2.1])
            elif select == 3:
                self.heart_speed = random.choice([0.8, 1.3, 1.8, 2.3, 2.8])

        # Heart 및 RainbowHeart는 생성 위치 및 각이 좀 더 두리안이 먹기 편하게 조정함
        if self.heart_spawnPoint == 'LEFT':
            self.heart_x_pos = -self.heart_width
            self.heart_y_pos = random.randint(100, screen_height-100-self.heart_height)
            self.heart_rad = random.choice([(1,1.5), (1,1), (1,0), (1.5,1), (1,-1), (1,-1.5), (1.5,-1)])
        elif self.heart_spawnPoint == 'RIGHT':
            self.heart_x_pos = screen_width
            self.heart_y_pos = random.randint(100, screen_height-100-self.heart_height)
            self.heart_rad = random.choice([(-1,1.5), (-1,1), (-1,0), (-1.5,1), (-1,-1), (-1,-1.5), (-1.5,-1)])
        elif self.heart_spawnPoint == 'UP':
            self.heart_x_pos = random.randint(100, screen_width-100-self.heart_width)
            self.heart_y_pos = -self.heart_height
            self.heart_rad = random.choice([(1.5,1), (1,1), (1,1.5), (0,1), (-1,1), (-1,1.5), (-1.5,1)])
        elif self.heart_spawnPoint == 'DOWN':
            self.heart_x_pos = random.randint(100, screen_width-100-self.heart_width)
            self.heart_y_pos = screen_height
            self.heart_rad = random.choice([(1.5,-1), (1,-1), (1,-1.5), (0,-1), (-1,-1.5), (-1,-1), (-1.5,-1)])

    def heart_move(self):
        self.heart_x_pos += self.heart_speed * self.heart_rad[0]
        self.heart_y_pos += self.heart_speed * self.heart_rad[1]
        global bonus
        
        def reach_up():
            if self.heart_y_pos < -self.heart_height:
                return True
        
        def reach_down():
            if self.heart_y_pos > screen_height:
                return True
        
        def reach_left():
            if self.heart_x_pos < -self.heart_width:
                return True
        
        def reach_right():
            if self.heart_x_pos > screen_width:
                return True

        # Heart 및 RainbowHeart 가 화면 끝에 다다랐을 때 기능 각각 정의
        if self.rainbow_check:
            if self.heart_spawnPoint == 'UP':
                if reach_left() or reach_right() or reach_down():
                    rainbowHeart_list.remove(self)

            if self.heart_spawnPoint == 'DOWN':
                if reach_left() or reach_right() or reach_up():
                    rainbowHeart_list.remove(self)

            if self.heart_spawnPoint == 'LEFT':
                if reach_up() or reach_down() or reach_right():
                    rainbowHeart_list.remove(self)

            if self.heart_spawnPoint == 'RIGHT':
                if reach_up() or reach_down() or reach_left():
                    rainbowHeart_list.remove(self)
        else:
            if self.heart_spawnPoint == 'UP':
                if reach_left() or reach_right() or reach_down():
                    heart_list.remove(self)

            if self.heart_spawnPoint == 'DOWN':
                if reach_left() or reach_right() or reach_up():
                    heart_list.remove(self)

            if self.heart_spawnPoint == 'LEFT':
                if reach_up() or reach_down() or reach_right():
                    heart_list.remove(self)

            if self.heart_spawnPoint == 'RIGHT':
                if reach_up() or reach_down() or reach_left():
                    heart_list.remove(self)

    def heart_bump(self):
        self.heart_rect = self.heart_image.get_rect()
        self.heart_rect.left = self.heart_x_pos
        self.heart_rect.top = self.heart_y_pos

# 난이도 조절 기능
def level_choice(select):
    global levelStep, level, total_level_list, result, bonus, rainbowBonus, durian_hp
    
    # 점수 및 레벨구간 설정
    level = 0   # 적 숫자 결정인자
    result = 0  # 초기/리셋 스코어
    bonus = 0   # 초기/리셋 보너스 점수
    rainbowBonus = 0    # 초기/리셋 보너스 점수
    
    # 난이도에 따른 레벨구간들
    if select == 1:
        durian_hp = 3   # 초기/리셋 두리안 목숨
        levelStep = 10
        total_level_list = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 1000000]
    elif select == 2:
        durian_hp = 2   # 초기/리셋 두리안 목숨
        levelStep = 15
        total_level_list = [30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 350, 400, 450, 500, 1000000]
    elif select == 3:
        durian_hp = 1   # 초기/리셋 두리안 목숨
        levelStep = 20
        total_level_list = [20, 40, 60, 80, 100, 120, 140, 160, 180, 200, 250, 300, 350, 400, 1000000]
    
    
# 초기 세팅 = 기본 레벨 (난이도 1)
select = 1
level_choice(select)

# 메인화면    
def main():
    global enemy_list, heart_list, rainbowHeart_list, durian_x_pos, durian_y_pos, endgame
    
    # 플레이어 위치 리셋
    durian_x_pos = (screen_width/2) - (durian_width/2)  # 캐릭터의 x좌표 (캐릭터 중심기준)
    durian_y_pos = (screen_height/2) - (durian_height/2)    # 캐릭터의 y좌표 (캐릭터 중심기준)
    
    # Enemy / Heart / rainbowHeart를 담을 리스트 생성 및 리셋
    enemy_list = list()
    heart_list = list()
    rainbowHeart_list = list()
    
    start_space = True
    
    while start_space:
        FPS = time.tick(60)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                endgame = True
                start_space = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    play(select)
                    start_space = False
                elif event.key == pygame.K_F1:
                    info()
                    start_space = False
                    
        screen.blit(background, (0,0))
        screen.blit(durian, (durian_x_pos, durian_y_pos))
        
        text("TN Universe", (255,255,255), 300, 120)
        text("Press a  'Space key'  to play", (255,255,255), 300, 390)
        text("Press a  'F1'  to Info / Option", (255,255,255), 300, 480)
        
        pygame.display.update()
        
        
# 게임 내 객체들에 관한 설명 및 난이도 조절 창
def info():
    global select, endgame
    enemy_image_forInfo = pygame.image.load("img\\Enemy.png")
    heart_image_forInfo = pygame.image.load("img\\Heart.png")
    rainbowHeart_image_forInfo = pygame.image.load("img\\RainbowHeart.png")
    
    info_space = True
    
    while info_space:
        
        FPS = time.tick(60)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                endgame = True
                info_space = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    info_space = False
                    main()
                elif event.key == pygame.K_UP:
                    select += 1
                    if select > 3: select = 1
                    level_choice(select)
                elif event.key == pygame.K_DOWN:
                    select -= 1
                    if select < 1: select = 3
                    level_choice(select)
                    
        screen.blit(background, (0,0))
        screen.blit(durian, (180, 400))
        screen.blit(enemy_image_forInfo, (180,440))
        screen.blit(heart_image_forInfo, (180,480))
        screen.blit(rainbowHeart_image_forInfo, (180,520))
        text("TN Universe", (255,255,255), 300, 120)
        text("Press a  'Space key'  to main", (255,255,255), 300, 250)
        text("Select Level (Up/Down key):  "+str(select), (255,255,255), 300, 330)
        text("Mr.Durian", (255,255,255), 350, 400)
        text("Enemy", (255,255,255), 350, 440)
        text("Heart (Bonus+10)", (255, 255, 255), 350, 480)
        text("RainbowHeart (Bonus+50)", (255, 255, 255), 350, 520)
        
        pygame.display.update()

        
# 게임오버 시 나타나는 창
def gameover(score, recentSelect, bonusScore):
    global endgame
    
    gameover_space = True
    
    while gameover_space:
        FPS = time.tick(60)
        
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                endgame = True
                gameover_space = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    gameover_space = False
                    level_choice(select)
                    main()
        
        screen.blit(background, (0,0))
        
        text("Game Over", (255,255,255), 300, 120)
        text("Press a  'Space key'  to main", (255,255,255), 300, 400)
        text("Score: " + str(score+bonusScore) + " / Level: " + str(recentSelect), (255,255,255), 300, 300)
            
        pygame.display.update()
    
                    
# 각종 메세지 표현 기능
def text(text, color, x, y):
        text_content = game_font.render(text, True, color)
        text_rect = text_content.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_content, text_rect)


# Game 플레이 부분
def play(select):
    global durian_x_pos, durian_y_pos, player_to_x, player_to_y, level, bonus, durian_hp, endgame
    
    boom_count=0
    heartLevel = 0
    isBoom = False
    
    running = True
    while running:
        FPS = time.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                endgame = True
                running = False

            # Key를 press하는 동안 speed만큼씩 움직임
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_to_x -= durian_speed
                if event.key == pygame.K_RIGHT:
                    player_to_x += durian_speed
                if event.key == pygame.K_UP:
                    player_to_y -= durian_speed
                if event.key == pygame.K_DOWN:
                    player_to_y += durian_speed
                
            # Key에서 Release되면 제자리에 멈춤
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_LEFT, pygame.K_RIGHT]:
                    player_to_x = 0
                if event.key in [pygame.K_UP, pygame.K_DOWN]:
                    player_to_y = 0
        
        # player가 해당 좌표에 표현되는 프레임속도 값 == 끊김없이 표현될 수 있게 하는 기능
        durian_x_pos += player_to_x * FPS
        durian_y_pos += player_to_y * FPS


        # 플레이어 경계값
        if durian_x_pos < 0:
            durian_x_pos = 0
        elif durian_x_pos > screen_width - durian_width:
            durian_x_pos = screen_width - durian_width
        if durian_y_pos < 0:
            durian_y_pos = 0
        elif durian_y_pos > screen_height - durian_height:
            durian_y_pos = screen_height - durian_height

        # Enemy 생성 기능(난이도에 따라 속도 및 개수 조절)
        if result >= total_level_list[level]:
            level += 1

        if level + levelStep >= len(enemy_list):
            enemy_list.append(Enemy(select))
            
        # Heart 또는 RainbowHeart 생성 기능(난이도에 따라 속도 및 개수 조절)
        if select == 1: heartLevel = 5
        elif select == 2: heartLevel = 3
        elif select == 1: heartLevel = 1
        
        if heartLevel >= len(heart_list) + len(rainbowHeart_list):
            heart_or_Rheart = Heart(select)
            if heart_or_Rheart.rainbow_check:
                rainbowHeart_list.append(heart_or_Rheart)
            else:
                heart_list.append(heart_or_Rheart)

        # 충돌 처리
        durian_character = durian.get_rect()
        durian_character.left = durian_x_pos
        durian_character.top = durian_y_pos

        # Enemy 부딪치면 게임오버
        for count in enemy_list:
            count.enemy_bump()
            if durian_character.colliderect(count.enemy_rect):
                isBoom = True
                if durian_hp == 3:
                    durian_hp=2
                    enemy_list.remove(count)
                elif durian_hp == 2:
                    durian_hp=1
                    enemy_list.remove(count)
                elif durian_hp == 1:
                    durian_hp=0
                    enemy_list.remove(count)
                else:
                    running = False
                    gameover(result, select, bonus)
                
        # Heart 부딪치면 (보너스 점수+10)
        for count in heart_list:
            count.heart_bump()
            if durian_character.colliderect(count.heart_rect):
                heart_list.remove(count)
                bonus += 10
                
        # RainbowHeart 부딪치면 (보너스 점수+50)
        for count in rainbowHeart_list:
            count.heart_bump()
            if durian_character.colliderect(count.heart_rect):
                rainbowHeart_list.remove(count)
                bonus += 50

        # 화면에 게임 나타내기!!
        screen.blit(background, (0, 0))
        screen.blit(durian, (durian_x_pos, durian_y_pos))
        
        if isBoom:
            screen.blit(boom,(durian_x_pos-5,durian_y_pos-5))
            boom_count += 1
            if boom_count > 7:
                boom_count = 0
                isBoom = False

        for count in enemy_list:
            count.enemy_move()
            screen.blit(count.enemy_image, (count.enemy_x_pos, count.enemy_y_pos))
            
        for count in heart_list:
            count.heart_move()
            screen.blit(count.heart_image, (count.heart_x_pos, count.heart_y_pos))
            
        for count in rainbowHeart_list:
            count.heart_move()
            screen.blit(count.heart_image, (count.heart_x_pos, count.heart_y_pos))
            
        
        text("Enemy count", (255,255,255), 50, 10)
        enemy_count = game_font.render(str(len(enemy_list)), True, (255, 255, 255))
        screen.blit(enemy_count, (30, 30))
        
        text("Level: ", (255,255,255), 200, 10)
        selectbar = game_font.render(str(select), True, (255, 255, 255))
        screen.blit(selectbar, (230, 10))
        
        text("HP: ", (255,255,255), 340, 10)
        hpbar = game_font.render(str(durian_hp), True, (255, 255, 255))
        screen.blit(hpbar, (370, 10))

        text("Score", (255,255,255), screen_width - 50, 10)
        score = game_font.render(str(int(result)), True, (255, 255, 255))
        screen.blit(score, (screen_width - 60, 30))
        
        text("Bonus", (255,255,255), screen_width - 100, 10)
        bonusScore = game_font.render(str(int(bonus)), True, (255, 255, 255))
        screen.blit(bonusScore, (screen_width - 110, 30))

        pygame.display.update()


if endgame: pygame.quit()


# 게임 Start!!
main()
    
    
    
# Mr. Woo
# TN Co.