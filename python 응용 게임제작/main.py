import os
import pygame as pg
import math
import time
import random


# 초기 설정
pg.init()
pg.mixer.init()
screen_width = 1280  # 화면의 너비
screen_height = 720   # 화면의 높이
screen = pg.display.set_mode((screen_width, screen_height))  # 화면 크기 설정
pg.display.set_caption("NERTAMIGHT")  # 창 제목 설정
clock = pg.time.Clock()  # FPS를 조절하기 위한 클락 객체 생성

#효과음 로드
current_path = os.path.dirname(__file__)
sound_path = os.path.join(current_path, "sounds")

bgm = os.path.join(sound_path, "고아원 배경 사운드.wav")
pg.mixer.music.load(bgm)
pg.mixer.music.set_volume(1.0)  # 음량을 최대(1.0)로 설정

pg.mixer.music.load(os.path.join(sound_path, "고아원 배경 사운드.wav"))
pg.mixer.music.play(-1)  # 무한 반복 재생


# 이미지 경로 설정
current_path = os.path.dirname(__file__)  # 현재 파일 경로
image_path = os.path.join(current_path, "images")  # 이미지 파일들이 위치할 경로

# 배경 이미지 로드
boss1room = pg.image.load(os.path.join(image_path, "그림02.png")) # 보스 스테이지 1
walkway = pg.image.load(os.path.join(image_path, '복도.png'))
boss2room = pg.image.load(os.path.join(image_path, "그림02.png")) # 보스 스테이지 2
bossfinal = pg.image.load(os.path.join(image_path, '보스룸마지막.png'))

class GATE:
    def __init__(self, x, y, image_path):
        self.image = pg.image.load(image_path)  # 문 이미지 로드
        self.rect = self.image.get_rect(center=(x, y))  # 문 위치 설정
        self.active = False  # 포탈 활성화 상태
        self.last_active_time = 0
        self.active_delay = 2000  # 활성화 대기 시간(ms)

    def draw_portal(self, screen):
        current_time = pg.time.get_ticks()
        if not self.active and current_time - self.last_active_time >= self.active_delay:
            self.active = True
            self.last_active_time = current_time  # 시간 갱신
        if self.active:
            screen.blit(self.image, self.rect)  # 문 이미지 그리기

# 문 이미지 경로 설정
door_image_path = os.path.join(image_path, "열린문.png")

# 포탈 객체 생성 (문 위치는 x=1230, y=360)
portal = GATE(1240, 360, door_image_path)

#스토리 이미지 설정
class STORY:
    def __init__(self):
        self.i = 0
        self.storys = [pg.image.load(os.path.join(image_path, f'스토리{i}.png'))for i in range(1, 6)]
        self.next_image_time = 2
        self.last_image_time = time.time()
    
    def Story(self):
        if time.time() - self.last_image_time >= self.next_image_time:
            self.last_image_time = time.time()
            self.i += 1
        if self.i >= len(self.storys):
                return False
        screen.blit(self.storys[self.i], (0, 0))
        return True

class ENDINGSTORY:
    def __init__(self):
        self.i = 0
        self.storys = [pg.image.load(os.path.join(image_path, f'엔딩스토리{i}.png'))for i in range(1, 4)]
        self.next_image_time = 2
        self.last_image_time = time.time()
    
    def Story(self):
        if time.time() - self.last_image_time >= self.next_image_time:
            self.last_image_time = time.time()
            self.i += 1
        if self.i >= len(self.storys):
                return False
        screen.blit(self.storys[self.i], (0, 0))
        return True

class Character:
    def __init__(self, image_path, x, y, speed, lives=3):
        # 캐릭터의 기본 속성 초기화
        self.image = pg.image.load(image_path)  # 캐릭터 이미지 로드
        self.rect = self.image.get_rect(center=(x, y))  # 캐릭터의 사각형 영역 생성
        self.speed = speed  # 캐릭터의 이동 속도
        self.lives = lives  # 캐릭터의 생명
        self.red_image = self.image.copy()  # 캐릭터의 붉은 이미지 복사
        self.red_image.fill((255, 0, 0), special_flags=pg.BLEND_MULT)  # 붉은 이미지 생성
        self.hit_timer = 0  # 맞았을 때의 타이머
        self.is_flipped = False # 이미지 반전 여부
        self.is_red_flipped = False # 붉은 이미지 반전 여부

    def move(self, dx, dy, dt):
        # 캐릭터 이동 메서드
        if self.hit_timer > 0:  # 맞은 상태라면
            self.hit_timer -= dt  # 타이머 감소
        self.rect.x += dx * self.speed * dt  # x축 이동
        self.rect.y += dy * self.speed * dt  # y축 이동
        self.rect.clamp_ip(screen.get_rect())  # 화면 경계에서 벗어나지 않도록 조정
        # 좌우 방향키 눌렀을 때 이미지 반전 처리
        if dx < 0 and not self.is_flipped: # 왼쪽으로 움직일 때
            self.red_image = pg.transform.flip(self.red_image, True, False)
            self.image = pg.transform.flip(self.image, True, False)
            self.is_flipped = True
            self.is_red_flipped = True
        elif dx > 0 and self.is_flipped: # 오른쪽으로 움직일 때
            self.red_image = pg.transform.flip(self.red_image, True, False)
            self.image = pg.transform.flip(self.image, True, False)
            self.is_red_flipped = False
            self.is_flipped = False

    def draw(self):
        # 캐릭터 그리기 메서드
        if self.hit_timer > 0:  # 맞은 상태라면
            screen.blit(self.red_image, self.rect)  # 붉은 이미지로 그리기
        else:
            screen.blit(self.image, self.rect)  # 일반 이미지로 그리기

    def hit(self):
        # 캐릭터가 맞았을 때의 처리
        if self.hit_timer <= 0:  # 무적 시간이 아닐 때만
            self.hit_timer = 1000  # 1초간 무적 상태 설정
            self.lives -= 1  # 생명 감소

class Ethan(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "에단.png"), x, y, 0.3)  # Ethan 초기화
        self.lives = 3  # 생명 수
        self.life_image = pg.image.load(os.path.join(image_path, '목숨.png'))  # 생명 이미지 로드
        self.life_width = self.life_image.get_width()  # 생명 이미지의 너비
        self.fires = []  # 발사한 불꽃 리스트
        self.fire_image = pg.image.load(os.path.join(image_path, '빛.png'))  # 불꽃 이미지 로드
        self.last_shoot_time = 0  # 마지막 발사 시간 저장
        self.shoot_delay = 200  # 200ms(0.2초) 간격으로 발사 가능
        self.facing_right = True
        #아이템 설정
        self.acttack_power = 1
        self.fire_size = 1.0
        self.heal = False
        self.last_heal_time = 0
    
    def shoot(self, direction, angle):
        # 불꽃 발사 메서드 (0.2초 딜레이 체크 추가)
        current_time = pg.time.get_ticks()
        if current_time - self.last_shoot_time >= self.shoot_delay:
            if self.facing_right:
                start_x = self.rect.centerx + 30
            else:
                start_x = self.rect.centerx - 27
            self.fires.append({"pos": [start_x, self.rect.centery], "dir": direction, "angle": angle})
            self.last_shoot_time = current_time  # 마지막 발사 시간 업데이트

    def update_fires(self, dt):
        # 발사한 불꽃 업데이트
        for fire in self.fires[:]:
            fire["pos"][0] += fire["dir"][0] * 0.3 * dt  # x축 이동
            fire["pos"][1] += fire["dir"][1] * 0.3 * dt  # y축 이동
            if not screen.get_rect().collidepoint(fire["pos"]):  # 화면을 벗어나면 삭제
                self.fires.remove(fire)

    def draw_fires(self):
        # 발사한 불꽃 그리기
        for fire in self.fires:
            rotated_fire = pg.transform.rotate(self.fire_image, fire["angle"])  # 불꽃 회전
            fire_rect = rotated_fire.get_rect(center=fire["pos"])  # 불꽃의 사각형 영역 생성
            screen.blit(rotated_fire, fire_rect)  # 불꽃 그리기

    def draw_lives(self, screen):
        # 오른쪽 상단에 Ethan의 목숨을 그림
        for i in range(self.lives):
            x = screen.get_width() - (i + 1) * (self.life_width + 10)  # 목숨 이미지 간격 설정
            y = 10  # 화면 상단에서 약간 띄운 위치
            screen.blit(self.life_image, (x, y))  # 목숨 이미지 그리기

    def collect_item(self, item):
        # 아이템 접촉시
        if self.rect.colliderect(item.rect):
            item.apply_effect(self)
            return True
        return False

# 유령
class Enemy1(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "몹1.png"), x, y, 0.05, 2)
        self.hp = 1
        self.red_duration = 1000
        self.red_timer = 0
        self.knockback_distance = 20  # 넉백 거리
    
    def update(self, dt):
        # 붉은 상태 업데이트
        if self.red_timer > 0:
            self.red_timer -= dt  # 타이머 감소

    def knockback(self, dx, dy):
        # 넉백 처리
        self.rect.x += dx  # x축으로 넉백
        self.rect.y += dy  # y축으로 넉백

    def update_position(self, target, dt):
        # Ethan을 추적하여 위치 업데이트
        dx, dy = target.rect.x - self.rect.x, target.rect.y - self.rect.y  # 목표와의 거리 계산
        distance = math.hypot(dx, dy)  # 거리 계산
        if distance != 0:
            self.move((dx / distance), (dy / distance), dt)
        self.rect.clamp_ip(screen.get_rect())  # 화면 경계에서 벗어나지 않도록 조정

    def draw(self):
        # 적 그리기 메서드
        if self.red_timer > 0:  # 붉은 상태라면
            screen.blit(self.red_image, self.rect)  # 붉은 적 이미지 그리기
        else:
            screen.blit(self.image, self.rect)  # 일반 적 이미지 그리기
            
    def hit(self):
        self.hp -= 1
        self.red_timer = self.red_duration
        if self.hp <= 0:
            return True
        return False
#촛불
class Enemy2(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "몹2.png"), x, y, 0.04, 2)
        self.hp = 2
        self.red_duration = 1000
        self.red_timer = 0
        self.knockback_distance = 20  # 넉백 거리
        self.flames = []  # 불꽃 정보 저장 (위치와 생성 시간)

    def update(self, dt):
        # 붉은 상태 업데이트
        if self.red_timer > 0:
            self.red_timer -= dt

        # 불꽃 지속 시간 관리
        current_time = pg.time.get_ticks()
        self.flames = [flame for flame in self.flames if current_time - flame["start_time"] < 3000]

    def knockback(self, dx, dy):
        # 넉백 처리
        self.rect.x += dx
        self.rect.y += dy

    def update_position(self, target, dt):
        # Ethan을 추적하여 위치 업데이트
        dx, dy = target.rect.x - self.rect.x, target.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.move((dx / distance), (dy / distance), dt)
        self.rect.clamp_ip(screen.get_rect())

    def draw(self):
        # Enemy2 그리기
        if self.red_timer > 0:
            screen.blit(self.red_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

        # 불꽃 그리기
        flame_image = pg.image.load(os.path.join(image_path, '불꽃.png'))  # 불꽃 이미지
        for flame in self.flames:
            flame_rect = flame_image.get_rect(center=flame["pos"])
            screen.blit(flame_image, flame_rect)

    def hit(self):
        # Enemy2가 공격을 받을 때
        self.hp -= 1
        self.red_timer = self.red_duration
        if self.hp <= 0:
            self.create_flame()  # 불꽃 생성
            return True
        return False

    def check_collision_with_ethan(self, ethan):
        # Ethan과 충돌했을 때 처리
        if self.rect.colliderect(ethan.rect):
            ethan.hit()
            self.create_flame()  # 불꽃 생성
            return True
        return False

    def create_flame(self):
        # 불꽃 생성 메서드
        self.flames.append({"pos": self.rect.center, "start_time": pg.time.get_ticks()})

#원장의 광신도
class Enemy3(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "몹3.png"), x, y, 0.05, 3)
        self.hp = 3
        self.red_duration = 1000
        self.red_timer = 0
        self.knockback_distance = 20  # 넉백 거리
    
    def update(self, dt):
        # 붉은 상태 업데이트
        if self.red_timer > 0:
            self.red_timer -= dt  # 타이머 감소

    def knockback(self, dx, dy):
        # 넉백 처리
        self.rect.x += dx  # x축으로 넉백
        self.rect.y += dy  # y축으로 넉백

    def update_position(self, target, dt):
        # Ethan을 추적하여 위치 업데이트
        dx, dy = target.rect.x - self.rect.x, target.rect.y - self.rect.y  # 목표와의 거리 계산
        distance = math.hypot(dx, dy)  # 거리 계산
        if distance != 0:
            self.move((dx / distance), (dy / distance), dt)
        self.rect.clamp_ip(screen.get_rect())  # 화면 경계에서 벗어나지 않도록 조정

    def draw(self):
        # 적 그리기 메서드
        if self.red_timer > 0:  # 붉은 상태라면
            screen.blit(self.red_image, self.rect)  # 붉은 적 이미지 그리기
        else:
            screen.blit(self.image, self.rect)  # 일반 적 이미지 그리기
            
    def hit(self):
        self.hp -= 1
        self.red_timer = self.red_duration
        if self.hp <= 0:
            return True
        return False

class Chaingoast(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, '체인유령.png'), x, y, 0.1, 50)  # Chaingoast 초기화
        self.hp = 50  # 체력
        self.red_duration = 1000  # 붉은 상태 지속 시간(ms)
        self.red_timer = 0  # 붉은 상태 타이머
        self.knockback_distance = 10  # 넉백 거리
        self.chains = []  # 체인 리스트
        self.chain_image = pg.image.load(os.path.join(image_path, '체인1.png'))  # 체인 이미지 로드
        self.attack_interval = 4  # 공격 간격(초)
        self.last_attack_time = time.time()  # 마지막 공격 시간
        self.drop = None # 드롭된 아이템 저장 변수

    def move(self, dx, dy, dt):
        super().move(dx, dy, dt)  # 부모 클래스의 move 메서드 호출
    
    def update(self, dt):
        # 붉은 상태 업데이트
        if self.red_timer > 0:
            self.red_timer -= dt  # 타이머 감소
    
    def knockback(self, dx, dy):
        # 넉백 처리
        self.rect.x += dx  # x축으로 넉백
        self.rect.y += dy  # y축으로 넉백

    def update_position(self, target, dt):
        # Ethan을 추적하여 위치 업데이트
        if boss_count:
            dx, dy = target.rect.x - self.rect.x, target.rect.y - self.rect.y  # 목표와의 거리 계산
            distance = math.hypot(dx, dy)  # 거리 계산
            if distance != 0:
                self.rect.x += (dx / distance) * self.speed * dt  # 목표 방향으로 이동
                self.rect.y += (dy / distance) * self.speed * dt  # 목표 방향으로 이동
            self.rect.clamp_ip(screen.get_rect())  # 화면 경계에서 벗어나지 않도록 조정

    def attack(self):
        # 체인 공격 메서드
        if time.time() - self.last_attack_time >= self.attack_interval:  # 공격 가능 시간 체크
            self.last_attack_time = time.time()  # 현재 시간을 마지막 공격 시간으로 설정
            for i in range(6):  # 6개의 체인 발사
                angle = 60 * i  # 각도 설정
                radians = math.radians(angle)  # 라디안 변환
                dir_x = math.cos(radians)  # x 방향
                dir_y = math.sin(radians)  # y 방향
                rotated_chain = pg.transform.rotate(self.chain_image, -angle)  # 체인 회전
                self.chains.append({
                    "pos": [self.rect.centerx, self.rect.centery],  # 체인 시작 위치
                    "dir": [dir_x, dir_y],  # 체인 방향
                    "image": rotated_chain  # 체인 이미지
                })

    def update_chains(self, dt):
        # 체인 업데이트
        for chain in self.chains:
            chain["pos"][0] += chain["dir"][0] * 0.3 * dt  # x축 이동
            chain["pos"][1] += chain["dir"][1] * 0.3 * dt  # y축 이동

    def draw_chains(self):
        # 체인 그리기
        for chain in self.chains:
            screen.blit(chain["image"], chain["pos"])  # 체인 이미지 그리기

    def draw(self):
        # Chaingoast 그리기 메서드
        if self.red_timer > 0:  # 붉은 상태라면
            screen.blit(self.red_image, self.rect)  # 붉은 유령 이미지 그리기
        else:
            screen.blit(self.image, self.rect)  # 일반 유령 이미지 그리기
            
        if self.drop:
            self.drop.draw()

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.item()  # 아이템 드랍
            return True
        return False

    def item(self):
        return Item(self.rect.centerx, self.rect.centery) # 아이템 생성 위치
#촛불 보스
class Candlelight(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "촛불유령.png"), x, y, 0.04, 50)
        self.hp = 50
        self.red_duration = 1000
        self.red_timer = 0
        self.fireballs = []  # Active fireballs list
        self.flames = []  # Active flames list
        self.fireball_image = pg.image.load(os.path.join(image_path, '불덩이.png'))  # 불덩이 이미지
        self.flame_image = pg.image.load(os.path.join(image_path, '불꽃.png'))  # 불꽃이미지
        self.fire_interval = 2000  # 1 초마다 불덩이 던짐
        self.last_fire_time = 0
        self.fireball_speed = 0.3  # 불덩이 속도

    def update(self, dt, ethan):
        if self.red_timer > 0:
            self.red_timer -= dt

        # Throw fireball if interval is met
        current_time = pg.time.get_ticks()
        if current_time - self.last_fire_time >= self.fire_interval:
            self.throw_fireball(ethan)
            self.last_fire_time = current_time

        # Update fireballs
        for fireball in self.fireballs[:]:
            # Update fireball position
            fireball["pos"][0] += fireball["velocity"][0] * dt
            fireball["pos"][1] += fireball["velocity"][1] * dt

            # Check if fireball has reached its target
            if math.hypot(
                fireball["pos"][0] - fireball["target"][0],
                fireball["pos"][1] - fireball["target"][1],
            ) < 5:
                self.create_flame(fireball["target"])  # Create flame at the target position
                self.fireballs.remove(fireball)

        # Update flames
        for flame in self.flames[:]:
            flame["duration"] -= dt
            if flame["duration"] <= 0:
                self.flames.remove(flame)

    def throw_fireball(self, ethan):
        # Calculate the target position (Ethan's position at the time of throwing)
        target_position = (ethan.rect.centerx, ethan.rect.centery)

        # Calculate velocity to move toward the target
        dx = target_position[0] - self.rect.centerx
        dy = target_position[1] - self.rect.centery
        distance = math.hypot(dx, dy)
        velocity = [(dx / distance) * self.fireball_speed, (dy / distance) * self.fireball_speed]

        # Calculate the angle of the fireball for rotation
        angle = math.degrees(math.atan2(dy, dx))

        # Add a fireball to the list
        fireball = {
            "pos": [self.rect.centerx, self.rect.centery],  # Start position of fireball
            "velocity": velocity,  # Direction and speed
            "target": target_position,  # Target position
            "angle": angle,  # Rotation angle
            "image": self.fireball_image,
        }
        self.fireballs.append(fireball)

    def create_flame(self, position):
        # Create a flame at the specified position
        flame = {
            "pos": position,
            "duration": 6000,  # Flame lasts for 10 seconds (in milliseconds)
        }
        self.flames.append(flame)

    def draw(self):
        # Draw Candlelight
        if self.red_timer > 0:
            screen.blit(self.red_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

        # Draw fireballs
        for fireball in self.fireballs:
            rotated_fireball = pg.transform.rotate(fireball["image"], -fireball["angle"])  # Rotate based on angle
            fireball_rect = rotated_fireball.get_rect(center=fireball["pos"])
            screen.blit(rotated_fireball, fireball_rect)

        # Draw flames
        for flame in self.flames:
            flame_rect = self.flame_image.get_rect(center=flame["pos"])
            screen.blit(self.flame_image, flame_rect)

    def hit(self):
        self.hp -= 1
        self.red_timer = self.red_duration
        if self.hp <= 0:
            return True
        return False

    def item(self):
        return Item(self.rect.centerx, self.rect.centery) # 아이템 생성 위치
class FinalBoss(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "원장.png"), x, y, 0.05, 50)
        self.hp = 50
        self.red_duration = 1000
        self.red_timer = 0
        self.fireballs = []  # 발사된 불꽃 리스트
        self.fireball_image = pg.image.load(os.path.join(image_path, "불덩리.png"))  # 불꽃 이미지
        self.last_fire_time = 0
        self.fire_interval = 1500  # 불꽃 발사 간격 (1.5초)
        self.fireball_speed = 0.3  # 불꽃 이동 속도

    def update(self, dt, ethan):
        # 보스가 에단을 추적
        self.follow_player(ethan, dt)

        # 불꽃 업데이트
        current_time = pg.time.get_ticks()
        if current_time - self.last_fire_time >= self.fire_interval:
            self.shoot_fireball(ethan)
            self.last_fire_time = current_time

        # 불꽃의 위치 업데이트
        for fireball in self.fireballs[:]:
            fireball["pos"][0] += fireball["velocity"][0] * dt
            fireball["pos"][1] += fireball["velocity"][1] * dt

            # 화면 밖으로 나가면 삭제
            if not screen.get_rect().collidepoint(fireball["pos"]):
                self.fireballs.remove(fireball)

    def follow_player(self, ethan, dt):
        # Ethan의 위치를 추적하여 이동
        dx, dy = ethan.rect.x - self.rect.x, ethan.rect.y - self.rect.y
        distance = math.hypot(dx, dy)
        if distance != 0:
            self.move((dx / distance), (dy / distance), dt)

    def shoot_fireball(self, ethan):
        # Ethan의 현재 위치를 타겟으로 불꽃 발사
        target_x, target_y = ethan.rect.centerx, ethan.rect.centery
        dx, dy = target_x - self.rect.centerx, target_y - self.rect.centery
        distance = math.hypot(dx, dy)
        velocity = [(dx / distance) * self.fireball_speed, (dy / distance) * self.fireball_speed]

        # 불꽃의 회전 각도 계산
        angle = math.degrees(math.atan2(-dy, dx))  # Pygame의 y축이 아래로 향하므로 -dy 사용

        # 불꽃 추가
        self.fireballs.append({
            "pos": [self.rect.centerx, self.rect.centery],
            "velocity": velocity,
            "angle": angle,  # 회전 각도 저장
        })

    def draw(self):
        # 보스 그리기
        if self.red_timer > 0:
            screen.blit(self.red_image, self.rect)
        else:
            screen.blit(self.image, self.rect)

        # 불꽃 그리기
        for fireball in self.fireballs:
            rotated_fireball = pg.transform.rotate(self.fireball_image, fireball["angle"])
            fire_rect = rotated_fireball.get_rect(center=fireball["pos"])
            screen.blit(rotated_fireball, fire_rect)

    def hit(self):
        self.hp -= 1
        self.red_timer = self.red_duration
        if self.hp <= 0:
            return True
        return False

    def item(self):
        return Item(self.rect.centerx, self.rect.centery) # 아이템 생성 위치
class LastBoss(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "원장1.png"), x, y, 0.05, 200)
        self.hp = 200  # 보스 체력
        self.red_duration = 1000  # 붉은 상태 지속 시간(ms)
        self.red_timer = 0  # 붉은 상태 타이머
        self.red_zones = []  # 빨간 판(경고 영역) 리스트
        self.lightning_strikes = []  # 벼락 리스트
        self.lightning_image = pg.image.load(os.path.join(image_path, "벼락1.png"))  # 벼락 이미지
        self.red_zone_image = pg.Surface((100, 100), pg.SRCALPHA)  # 빨간 판 이미지 생성 (투명 배경)
        pg.draw.rect(self.red_zone_image, (255, 0, 0, 128), self.red_zone_image.get_rect())  # 반투명 빨간 판
        self.zone_interval = 1000  # 빨간 판 생성 간격 (1초)
        self.last_zone_time = 0  # 마지막으로 빨간 판이 생성된 시간

    def update(self, dt, ethan):
        # 현재 시간 가져오기
        current_time = pg.time.get_ticks()

        # 특정 간격마다 빨간 판 생성
        if current_time - self.last_zone_time >= self.zone_interval:
            self.spawn_red_zone(4)
            self.last_zone_time = current_time

        # 빨간 판 타이머 업데이트
        for zone in self.red_zones[:]:
            zone["timer"] -= dt  # 타이머 감소
            if zone["timer"] <= 0:
                # 타이머가 0이 되면 벼락 생성 후 빨간 판 삭제
                self.spawn_lightning(zone["pos"], ethan)
                self.red_zones.remove(zone)

        # 벼락 타이머 업데이트
        for lightning in self.lightning_strikes[:]:
            lightning["timer"] -= dt  # 타이머 감소
            if lightning["timer"] <= 0:
                self.lightning_strikes.remove(lightning)  # 타이머가 끝나면 벼락 삭제

    def spawn_red_zone(self, count):
        # 화면 내 랜덤 위치에 빨간 판 생성
        for _ in range(count):
            x = random.randint(80, screen_width - 230)
            y = random.randint(240, screen_height - 150)
            self.red_zones.append({"pos": (x, y), "timer": 1000})  # 빨간 판 위치와 1초 타이머 설정

    def spawn_lightning(self, red_zone_position, ethan):
        # 벼락 생성 메서드
        for _ in range(4):
            lightning_x = red_zone_position[0] + 1.5  # 붉은 판과 벼락의 중심 정렬
            lightning_y = red_zone_position[1] - 620  # 벼락의 아랫면을 붉은 판에 맞춤
            lightning_rect = self.lightning_image.get_rect(topleft=(lightning_x, lightning_y))  # 벼락 위치 설정
            self.lightning_strikes.append({"rect": lightning_rect, "timer": 1000})  # 벼락을 1초 동안 표시
            if ethan.rect.colliderect(lightning_rect):  # Ethan과 벼락 충돌 확인
                ethan.hit()  # Ethan이 맞았을 때 체력 감소 처리

    def draw(self):
        # 보스와 빨간 판 그리기
        super().draw()  # 부모 클래스의 draw 호출 (보스 이미지 그리기)

        # 빨간 판 그리기
        for zone in self.red_zones:
            screen.blit(self.red_zone_image, zone["pos"])  # 빨간 판 그리기

        # 벼락 그리기
        for lightning in self.lightning_strikes:
            screen.blit(self.lightning_image, lightning["rect"])  # 벼락 이미지 그리기
    
    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.item()  # 아이템 드랍
            return True
        return False
    
    def item(self):
        return Item(self.rect.centerx, self.rect.centery) # 아이템 생성 위치


#랜덤 아이템
class Item():
    def __init__(self, x, y):
        self.types = ['health', 'attack', 'speed', 'fire_size', 'heal']
        self.type = random.choice(self.types) # 랜덤으로 아이템 타입 설정
        self.image = pg.image.load(os.path.join(image_path, f"{self.type}.png"))  # 각 아이템에 맞는 이미지 로드
        self.rect = self.image.get_rect(center=(x, y))  # 아이템 위치 설정

    def apply_effect(self, ethan):
        # 아이템 효과를 Ethan에게 적용
        if self.type == 'health':
            ethan.lives += 1
        elif self.type == 'attack':
            ethan.attack_power += 1
        elif self.type == 'speed':
            ethan.speed += 0.1
        elif self.type == 'fire_size':
            ethan.fire_size_multiplier = 1.7
        elif self.type == 'heal':
            ethan.regen_enabled = True

    def draw(self):
        # 아이템을 화면에 그림
        screen.blit(self.image, self.rect)

font = pg.font.Font(None, 100)#폰트 객체 생성(폰트, 크기)
title_text = font.render("NERTAMIGHT", True, (255, 255, 255))
start_text = font.render("START", True, (0, 255, 0))
title_rect = title_text.get_rect(center=(screen_width / 2, screen_height / 3))
start_rect = start_text.get_rect(center=(screen_width / 2, screen_height / 2))
portal_font = pg.font.Font(None, 30)
move_text = portal_font.render("go to next stage? : Y", True, (255, 255, 255))
move_rect = move_text.get_rect(center = (640, 380))
dt = clock.tick(60)
map_move = 0
boss_count = False

def retry():
    running = 1
    while running:
        screen.fill((0, 0, 0))  # 화면을 검정색으로 채움
        die_text = font.render("YOU DIED", True, (255, 0, 0))
        die_rect = die_text.get_rect(center=(screen_width / 2, screen_height / 2))
        screen.blit(die_text, die_rect)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        pg.display.update()  # 화면 업데이트


# 게임 루프 및 충돌 처리
def main():
    global dt,map_move
    ethan = Ethan(screen_width / 2, screen_height / 2)  # Ethan 객체 생성
    
    # 텍스트 업데이트 함수
    def update_text(current, target):
        # 현재 텍스트에서 목표 텍스트로 한 글자씩 변경
        for i in range(len(target)):
            if current[i] != target[i]:
                current = current[:i] + target[i] + current[i + 1:]
            yield current

    # 엔딩 함수 수정
    def ending():
        story = ENDINGSTORY()
        current_text = "NERTMIGHT"
        target_text = "NIGHTMARE"
        text_gen = update_text(current_text, target_text)
        final_title = font.render(target_text, True, (255, 255, 255))

        running = True
        while running:
            screen.fill((0, 0, 0))
        
            if not story.Story():
                # 스토리 이미지가 끝난 후 텍스트 변경
                try:
                    # 텍스트가 변경 중이면 한 글자씩 진행
                    current_text = next(text_gen)
                except StopIteration:
                    # 텍스트 변경 완료 후
                    running = False

                title_text = font.render(current_text, True, (255, 255, 255))
                screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, screen_height / 2))
            else:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        running = False
                        return

            pg.display.update()
            clock.tick(2)  # 텍스트 업데이트 속도 조절

    
    def stage3():
                #1스테이지
        enemies = []  # 등장한 적 리스트
        start_time = time.time()  # 스테이지 시작 시간
        enemy_spawn_interval = 3  # 적 등장 간격 (초)
        total_duration = 60  # 3분 동안 적이 등장
        last_spawn_time = start_time  # 마지막 적 등장 시간
        running = True
        portal_created = False  # 포탈 생성 여부
        portal.active = False
        
        # 충돌 처리
        
        while running:
            dt = clock.tick(60)
            
            screen.blit(walkway, (0,0))
            ethan.draw()
            ethan.draw_lives(screen)
            
            elapsed_time = time.time() - start_time  # 스테이지 경과 시간
            remaining_time = max(0, total_duration - elapsed_time) # 남은 시간
            timer_test = font.render(f'{int(remaining_time)}', True, (255, 255, 255)) #남은 시간 화면에 표시
            screen.blit(timer_test, ((screen_width / 2) - 30, 10))
            
            # 3분이 경과하면 포탈 생성
            if elapsed_time >= total_duration and not portal_created:
                portal.active = True
                portal_created = True

        # 3초마다 적이 등장하고, 3분 동안만 적 등장
            if elapsed_time < total_duration and time.time() - last_spawn_time >= enemy_spawn_interval:
                new_enemy = Enemy3(random.randrange(0,1281), random.randrange(0,721))  # 새로운 적 생성
                enemies.append(new_enemy)
                last_spawn_time = time.time()  # 마지막 적 등장 시간 업데이트

            #이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1

            keys = pg.key.get_pressed()  # 현재 눌린 키 확인
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)  # 캐릭터 이동

            # 불꽃 이동 및 충돌 처리
            ethan.update_fires(dt)  # 불꽃 업데이트
            ethan.draw_fires()  # 불꽃 그리기
            
            #빛 유령 충돌처리
            # 적 이동, 불꽃과의 충돌 검사 및 그리기
            for enemy in enemies[:]:  # 적 리스트 복사본 사용
                enemy.update(dt)
                enemy.update_position(ethan, dt)
                enemy.draw()
                
                if ethan.rect.colliderect(enemy.rect):
                    ethan.hit()

                # 불꽃과 적의 충돌 검사
                for fire in ethan.fires[:]:
                    if enemy.rect.collidepoint(fire["pos"]):
                        #넉백처리
                        knockback_x = (enemy.rect.centerx - ethan.rect.centerx) / math.hypot(enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery) * enemy.knockback_distance
                        knockback_y = (enemy.rect.centery - ethan.rect.centery) / math.hypot(enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery) * enemy.knockback_distance
                        enemy.knockback(knockback_x, knockback_y)
                        ethan.fires.remove(fire)  # 충돌한 불꽃 삭제
                        if enemy.hit():
                            enemies.remove(enemy)  # lives가 0 이하이면 적 삭제
                        break
            
            
            # 적 이동 및 그리기
            for enemy in enemies:
                enemy.update_position(ethan, dt)
                dx = ethan.rect.x - enemy.rect.x
                if dx != 0:
                    enemy.move((ethan.rect.x - enemy.rect.x) / abs(ethan.rect.x - enemy.rect.x), 0, dt)  # 좌우 움직임 반영
                    # 적 좌우 이동 시 이미지 반전 처리
                    if (ethan.rect.x - enemy.rect.x) < 0 and not enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = True
                    elif (ethan.rect.x - enemy.rect.x) > 0 and enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = False
                else:
                    enemy.move(0,0, dt)
                enemy.draw()

            # 포탈 그리기
            if portal.active :
                portal.draw_portal(screen)
                if ethan.rect.colliderect(portal.rect):
                    screen.blit(move_text, move_rect)
                    if keys[pg.K_y]:  # Y 키를 누르면 이동
                        stage3_boss()
                        running = False
                    
            # Ethan이 죽으면 retry 화면으로 이동
            if ethan.lives <= 0:
                running = False
                retry()
        
            pg.display.update()  # 화면 업데이트
    
    def boss():
    
        lastboss = LastBoss(screen_width // 2, 150)
        running = True

        while running:
            dt = clock.tick(60)
            screen.blit(bossfinal, (0, 0))  # 새로운 배경 이미지

            # 이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1
            
            # Ethan 이동
            keys = pg.key.get_pressed()
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)

            # Ethan의 불꽃 업데이트
            ethan.update_fires(dt)
            ethan.draw_fires()


            # 최종 보스 로직 업데이트 및 그리기
            if lastboss.hp > 0:
                lastboss.update(dt, ethan)  # 보스 업데이트 (빨간 판과 벼락)
                lastboss.draw()  # 보스 및 빨간 판 그리기

                # Ethan의 불꽃과 보스 충돌 체크
                for fire in ethan.fires[:]:
                    if lastboss.rect.collidepoint(fire["pos"]):  # 불꽃이 보스에 맞았을 때
                        ethan.fires.remove(fire)  # 불꽃 삭제
                        if lastboss.hit():  # 보스 체력 감소
                            ending()
                            running = False  # 보스가 죽으면 루프 종료

                # 보스 체력바 그리기
                hp_bar_width = 300 * (lastboss.hp / 200)  # 체력 비율 계산
                pg.draw.rect(screen, (100, 100, 100), ((screen_width - 300) / 2, 30, 300, 20))  # 체력바 배경
                pg.draw.rect(screen, (255, 0, 0), ((screen_width - 300) / 2, 30, hp_bar_width, 20))  # 체력바


            # 에단과 그리기
            ethan.draw()


            # 에단 체력 그리기
            ethan.draw_lives(screen)

            # 에단 죽음 처리
            if ethan.lives <= 0:
                retry()
                running = False  # 에단이 죽으면 종료

            pg.display.update()

    def stage3_boss():
        ethan = Ethan(screen_width / 2, screen_height / 2)  # Ethan 생성
        final_boss = FinalBoss(screen_width / 2, screen_height / 4)  # FinalBoss 생성
        global boss_count
        boss_count = True

        running = True
        while running and boss_count:
            dt = clock.tick(60)
            screen.blit(boss2room, (0, 0))

            # 이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1
            
            # Ethan 이동
            keys = pg.key.get_pressed()
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)

            # Ethan의 불꽃 업데이트
            ethan.update_fires(dt)
            ethan.draw_fires()

            # FinalBoss 로직 업데이트
            final_boss.update(dt, ethan)
            final_boss.draw()

            # Ethan의 불꽃과 FinalBoss 충돌 체크
            for fire in ethan.fires[:]:
                if final_boss.rect.collidepoint(fire["pos"]):
                    ethan.fires.remove(fire)
                    if final_boss.hit():
                        boss_count = False  # 보스 죽음
                        boss()
                        running = False

            # FinalBoss의 불꽃과 Ethan 충돌 체크
            for fireball in final_boss.fireballs:
                fire_rect = final_boss.fireball_image.get_rect(center=fireball["pos"])
                if ethan.rect.colliderect(fire_rect):
                    ethan.hit()

            # Ethan의 체력 확인
            if ethan.lives <= 0:
                running = False
                retry()  # 게임 오버 화면

            # 보스 체력 표시
            hp_bar_width = 300 * (final_boss.hp / 50)
            pg.draw.rect(screen, (100, 100, 100), ((screen_width - 300) / 2, 30, 300, 20))  # 배경 바
            pg.draw.rect(screen, (255, 0, 0), ((screen_width - 300) / 2, 30, hp_bar_width, 20))  # 체력 바

            # Ethan 그리기
            ethan.draw()
            ethan.draw_lives(screen)

            pg.display.update()
    
    def stage2():
        #2스테이지
        enemies = []  # 등장한 적 리스트
        start_time = time.time()  # 스테이지 시작 시간
        enemy_spawn_interval = 5  # 적 등장 간격 (초)
        total_duration = 60  # 1분 동안 적이 등장
        last_spawn_time = start_time  # 마지막 적 등장 시간
        running = True
        portal_created = False  # 포탈 생성 여부
        portal.active = False
        
        
        while running:
            dt = clock.tick(60)
            
            screen.blit(walkway, (0,0))
            ethan.draw()
            ethan.draw_lives(screen)
            
            elapsed_time = time.time() - start_time  # 스테이지 경과 시간
            remaining_time = max(0, total_duration - elapsed_time) # 남은 시간
            timer_test = font.render(f'{int(remaining_time)}', True, (255, 255, 255)) #남은 시간 화면에 표시
            screen.blit(timer_test, ((screen_width / 2) - 30, 10))
            
            # 3분이 경과하면 포탈 생성
            if elapsed_time >= total_duration and not portal_created:
                portal.active = True
                portal_created = True

        # 3초마다 적이 등장하고, 3분 동안만 적 등장
            if elapsed_time < total_duration and time.time() - last_spawn_time >= enemy_spawn_interval:
                new_enemy = Enemy2(random.randrange(0,1281), random.randrange(0,721))  # 새로운 적 생성
                enemies.append(new_enemy)
                last_spawn_time = time.time()  # 마지막 적 등장 시간 업데이트

            #이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1

            keys = pg.key.get_pressed()  # 현재 눌린 키 확인
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)  # 캐릭터 이동

            # 불꽃 이동 및 충돌 처리
            ethan.update_fires(dt)  # 불꽃 업데이트
            ethan.draw_fires()  # 불꽃 그리기
            
            #빛 유령 충돌처리
            # 적 이동, 불꽃과의 충돌 검사 및 그리기
            for enemy in enemies[:]:  # 적 리스트 복사본 사용
                enemy.update(dt)
                enemy.update_position(ethan, dt)
                enemy.draw()

                # Ethan과 몹의 충돌 처리
                if ethan.rect.colliderect(enemy.rect):
                    ethan.hit()  # Ethan 체력 감소
                    enemies.remove(enemy)  # 충돌한 몹 삭제

                # 불꽃과 적의 충돌 처리
                for fire in ethan.fires[:]:
                    if enemy.rect.collidepoint(fire["pos"]):
                        # 넉백 처리
                        knockback_x = (enemy.rect.centerx - ethan.rect.centerx) / math.hypot(
                            enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery
                        ) * enemy.knockback_distance
                        knockback_y = (enemy.rect.centery - ethan.rect.centery) / math.hypot(
                        enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery
                        ) * enemy.knockback_distance
                        enemy.knockback(knockback_x, knockback_y)
                        ethan.fires.remove(fire)  # 충돌한 불꽃 삭제
                        if enemy.hit():
                            enemies.remove(enemy)  # lives가 0 이하이면 적 삭제
                        break
            
            
            # 적 이동 및 그리기
            for enemy in enemies:
                enemy.update_position(ethan, dt)
                dx = ethan.rect.x - enemy.rect.x
                if dx != 0:
                    enemy.move((ethan.rect.x - enemy.rect.x) / abs(ethan.rect.x - enemy.rect.x), 0, dt)  # 좌우 움직임 반영
                    # 적 좌우 이동 시 이미지 반전 처리
                    if (ethan.rect.x - enemy.rect.x) < 0 and not enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = True
                    elif (ethan.rect.x - enemy.rect.x) > 0 and enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = False
                else:
                    enemy.move(0,0, dt)
                enemy.draw()

            # 포탈 그리기
            if portal.active :
                portal.draw_portal(screen)
                if ethan.rect.colliderect(portal.rect):
                    screen.blit(move_text, move_rect)
                    if keys[pg.K_y]:  # Y 키를 누르면 이동
                        stage2_boss()
                        running = False
                    
            # Ethan이 죽으면 retry 화면으로 이동
            if ethan.lives <= 0:
                running = False
                retry()
        
            pg.display.update()  # 화면 업데이트
    
    def stage2_boss():
        ethan = Ethan(screen_width / 2, (screen_height / 2) - 200)  # Ethan 객체 생성
        candle = Candlelight(screen_width / 2, screen_height / 2)
        global boss_count
        boss_count = True
        start_time = time.time()
        portal_created = False  # 포탈 생성 여부
        portal.active = False
        #두번째 보스 촛불
        running = True
        while running & boss_count:
            dt = clock.tick(60)  # 초당 프레임 설정
            screen.blit(boss2room, (0, 0))  # 배경 그리기
            map_move = 0
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 2:
                boss_active = True
            else:
                boss_active = False
            
            # 이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1

            keys = pg.key.get_pressed()  # 현재 눌린 키 확인
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)  # 캐릭터 이동

            # 불꽃 이동 및 충돌 처리
            ethan.update_fires(dt)  # 불꽃 업데이트
            ethan.draw_fires()  # 불꽃 그리기
            
            if candle.hp > 0 and boss_active:
                candle.draw()
                for flame in candle.flames:
                    flame_rect = candle.flame_image.get_rect(center=flame["pos"])
                    if ethan.rect.colliderect(flame_rect):
                        ethan.hit()  # Ethan takes damage
                candle.update(dt, ethan)  # Update Candlelight's logic (including fireballs)

                # Candle 체력 게이지
                hp_bar_width = 300 * (candle.hp / 50)  # 체력 비율에 따른 게이지 너비 계산
                pg.draw.rect(screen, (100, 100, 100), ((screen_width - 300) / 2, 30, 300, 20))  # 배경 게이지
                pg.draw.rect(screen, (255, 0, 0), ((screen_width - 300) / 2, 30, hp_bar_width, 20))  # 체력 게이지
                
                # 충돌 처리
                if ethan.rect.colliderect(candle.rect):  # Ethan과 Chaingoast 충돌 처리
                    ethan.hit()  # Ethan의 hit 메서드 호출
                for fire in ethan.fires[:]:  # Ethan의 불꽃에 대해 충돌 처리
                    if candle.rect.collidepoint(fire["pos"]):  # Candle이 불꽃이 맞으면
                        candle.hit()  # Chaingoast의 체력 감소
                        ethan.fires.remove(fire)  # 불꽃 삭제
                        candle.red_timer = candle.red_duration  # Candle를 붉은 상태로 설정

            
            
            #포탈
            # 캐릭터와 포탈 충돌 검사
            else :
                portal.active = True
                portal.draw_portal(screen)
            #포탈 그리기
            if portal.active and ethan.rect.colliderect(portal.rect):
                screen.blit(move_text, move_rect)
                if map_move == 1:
                    stage3()
                    running = False
    
            # 캐릭터 그리기
            ethan.draw()  # Ethan 그리기
    
            # Ethan 체력 게이지
            ethan.draw_lives(screen)  # Ethan의 목숨 그리기
            if ethan.lives == 0:
                running = False
                retry()
    
            pg.display.update()  # 화면 업데이트
    
    def stage1():
        #1스테이지
        enemies = []  # 등장한 적 리스트
        start_time = time.time()  # 스테이지 시작 시간
        enemy_spawn_interval = 5  # 적 등장 간격 (초)
        total_duration = 60  # 3분 동안 적이 등장
        last_spawn_time = start_time  # 마지막 적 등장 시간
        running = True
        portal_created = False  # 포탈 생성 여부
        portal.active = False
        
        # 충돌 처리
        
        while running:
            dt = clock.tick(60)
            
            screen.blit(walkway, (0,0))
            ethan.draw()
            ethan.draw_lives(screen)
            
            elapsed_time = time.time() - start_time  # 스테이지 경과 시간
            remaining_time = max(0, total_duration - elapsed_time) # 남은 시간
            timer_test = font.render(f'{int(remaining_time)}', True, (255, 255, 255)) #남은 시간 화면에 표시
            screen.blit(timer_test, ((screen_width / 2) - 30, 10))
            
            # 3분이 경과하면 포탈 생성
            if elapsed_time >= total_duration and not portal_created:
                portal.active = True
                portal_created = True

        # 3초마다 적이 등장하고, 3분 동안만 적 등장
            if elapsed_time < total_duration and time.time() - last_spawn_time >= enemy_spawn_interval:
                new_enemy = Enemy1(random.randrange(0,1281), random.randrange(0,721))  # 새로운 적 생성
                enemies.append(new_enemy)
                last_spawn_time = time.time()  # 마지막 적 등장 시간 업데이트

            #이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1

            keys = pg.key.get_pressed()  # 현재 눌린 키 확인
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)  # 캐릭터 이동

            # 불꽃 이동 및 충돌 처리
            ethan.update_fires(dt)  # 불꽃 업데이트
            ethan.draw_fires()  # 불꽃 그리기
            
            #빛 유령 충돌처리
            # 적 이동, 불꽃과의 충돌 검사 및 그리기
            for enemy in enemies[:]:  # 적 리스트 복사본 사용
                enemy.update(dt)
                enemy.update_position(ethan, dt)
                enemy.draw()
                
                if ethan.rect.colliderect(enemy.rect):
                    ethan.hit()

                # 불꽃과 적의 충돌 검사
                for fire in ethan.fires[:]:
                    if enemy.rect.collidepoint(fire["pos"]):
                        #넉백처리
                        knockback_x = (enemy.rect.centerx - ethan.rect.centerx) / math.hypot(enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery) * enemy.knockback_distance
                        knockback_y = (enemy.rect.centery - ethan.rect.centery) / math.hypot(enemy.rect.centerx - ethan.rect.centerx, enemy.rect.centery - ethan.rect.centery) * enemy.knockback_distance
                        enemy.knockback(knockback_x, knockback_y)
                        ethan.fires.remove(fire)  # 충돌한 불꽃 삭제
                        if enemy.hit():
                            enemies.remove(enemy)  # lives가 0 이하이면 적 삭제
                        break
            
            
            # 적 이동 및 그리기
            for enemy in enemies:
                enemy.update_position(ethan, dt)
                dx = ethan.rect.x - enemy.rect.x
                if dx != 0:
                    enemy.move((ethan.rect.x - enemy.rect.x) / abs(ethan.rect.x - enemy.rect.x), 0, dt)  # 좌우 움직임 반영
                    # 적 좌우 이동 시 이미지 반전 처리
                    if (ethan.rect.x - enemy.rect.x) < 0 and not enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = True
                    elif (ethan.rect.x - enemy.rect.x) > 0 and enemy.is_flipped:
                        enemy.red_image = pg.transform.flip(enemy.red_image, True, False)
                        enemy.image = pg.transform.flip(enemy.image, True, False)
                        enemy.is_flipped = False
                else:
                    enemy.move(0,0, dt)
                enemy.draw()

            # 포탈 그리기
            if portal.active :
                portal.draw_portal(screen)
                if ethan.rect.colliderect(portal.rect):
                    screen.blit(move_text, move_rect)
                    if keys[pg.K_y]:  # Y 키를 누르면 이동
                        stage1_boss()
                        running = False
                    
            # Ethan이 죽으면 retry 화면으로 이동
            if ethan.lives <= 0:
                running = False
                retry()
        
            pg.display.update()  # 화면 업데이트
    
    def stage1_boss():
        ethan = Ethan(screen_width / 2, screen_height / 2)  # Ethan 객체 생성
        chaingoast = Chaingoast(screen_width / 2, screen_height / 2 - 200)  # Chaingoast 객체 생성
        global boss_count
        boss_count = True
        start_time = time.time()
        portal_created = False  # 포탈 생성 여부
        portal.active = False
        #첫 보스 체인 유령
        running = True
        while running & boss_count:
    
            dt = clock.tick(60)  # 초당 프레임 설정
            screen.blit(boss1room, (0, 0))  # 배경 그리기
            map_move = 0
            
            elapsed_time = time.time() - start_time
            if elapsed_time >= 2:
                boss_active = True
            else:
                boss_active = False
        

            # 이벤트 처리
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                if event.type == pg.KEYDOWN:  # 키 눌림 이벤트 처리
                    if event.key == pg.K_w:  # W 키를 누르면 위쪽으로 발사
                        ethan.shoot((0, -1), 90)
                    elif event.key == pg.K_s:  # S 키를 누르면 아래쪽으로 발사
                        ethan.shoot((0, 1), 270)
                    elif event.key == pg.K_a:  # A 키를 누르면 왼쪽으로 발사
                        ethan.shoot((-1, 0), 180)
                    elif event.key == pg.K_d:  # D 키를 누르면 오른쪽으로 발사
                        ethan.shoot((1, 0), 0)
                    elif event.key == pg.K_y: # Y 키를 누르면 이동
                        map_move = 1

            keys = pg.key.get_pressed()  # 현재 눌린 키 확인
            ethan.move((keys[pg.K_RIGHT] - keys[pg.K_LEFT]), (keys[pg.K_DOWN] - keys[pg.K_UP]), dt)  # 캐릭터 이동

            # 불꽃 이동 및 충돌 처리
            ethan.update_fires(dt)  # 불꽃 업데이트
            ethan.draw_fires()  # 불꽃 그리기
            
            if chaingoast.drop:
                Item.draw()
                if ethan.collect_item(chaingoast.drop):
                    chaingoast.drop = None

            if chaingoast.hp > 0:
                if (ethan.rect.x - chaingoast.rect.x) < 0 and not chaingoast.is_flipped:
                    chaingoast.red_image = pg.transform.flip(chaingoast.red_image, True, False)
                    chaingoast.image = pg.transform.flip(chaingoast.image, True, False)
                    chaingoast.is_flipped = True
                elif (ethan.rect.x - chaingoast.rect.x) > 0 and chaingoast.is_flipped:
                    chaingoast.red_image = pg.transform.flip(chaingoast.red_image, True, False)
                    chaingoast.image = pg.transform.flip(chaingoast.image, True, False)
                    chaingoast.is_flipped = False
                chaingoast.draw()  # Chaingoast 그리기
        
                # Chaingoast 체력 게이지
                hp_bar_width = 300 * (chaingoast.hp / 50)  # 체력 비율에 따른 게이지 너비 계산
                pg.draw.rect(screen, (100, 100, 100), ((screen_width - 300) / 2, 30, 300, 20))  # 배경 게이지
                pg.draw.rect(screen, (255, 0, 0), ((screen_width - 300) / 2, 30, hp_bar_width, 20))  # 체력 게이지
        
                if boss_active:
                # Chaingoast 행동 및 공격
                    chaingoast.update(dt)  # Chaingoast 업데이트
                    chaingoast.update_position(ethan, dt)  # Chaingoast가 Ethan을 추적
                    chaingoast.attack()  # Chaingoast 공격
                    chaingoast.update_chains(dt)  # 체인 업데이트
                    chaingoast.draw_chains()  # 체인 그리기

                # 충돌 처리
                if ethan.rect.colliderect(chaingoast.rect):  # Ethan과 Chaingoast 충돌 처리
                    ethan.hit()  # Ethan의 hit 메서드 호출
                for fire in ethan.fires[:]:  # Ethan의 불꽃에 대해 충돌 처리
                    if chaingoast.rect.collidepoint(fire["pos"]):  # Chaingoast에 불꽃이 맞으면
                        chaingoast.hit()  # Chaingoast의 체력 감소
                        ethan.fires.remove(fire)  # 불꽃 삭제

                        # 넉백 효과 추가
                        knockback_x = (chaingoast.rect.centerx - ethan.rect.centerx) / math.hypot(chaingoast.rect.centerx - ethan.rect.centerx, chaingoast.rect.centery - ethan.rect.centery) * chaingoast.knockback_distance
                        knockback_y = (chaingoast.rect.centery - ethan.rect.centery) / math.hypot(chaingoast.rect.centerx - ethan.rect.centerx, chaingoast.rect.centery - ethan.rect.centery) * chaingoast.knockback_distance
                        chaingoast.knockback(knockback_x, knockback_y)  # Chaingoast의 넉백 처리

                        chaingoast.red_timer = chaingoast.red_duration  # Chaingoast를 붉은 상태로 설정



                # 체인에 의한 충돌 처리
                for chain in chaingoast.chains:
                    if ethan.rect.collidepoint(chain["pos"]) and ethan.hit_timer <= 0:  # Ethan이 체인에 맞으면
                        ethan.hit()  # Ethan의 hit 메서드 호출

            #포탈
            # 캐릭터와 포탈 충돌 검사
            else :
                portal.active = True
                portal.draw_portal(screen)
            #포탈 그리기
            if portal.active and ethan.rect.colliderect(portal.rect):
                screen.blit(move_text, move_rect)
                if map_move == 1:
                    stage2()
                    running = False
    
            # 캐릭터 그리기
            ethan.draw()  # Ethan 그리기
    
            # Ethan 체력 게이지
            ethan.draw_lives(screen)  # Ethan의 목숨 그리기
            if ethan.lives == 0:
                running = False
                retry()
    
            pg.display.update()  # 화면 업데이트
    
    def story_screen():
        story = STORY()
        running = True
        while running:
            screen.fill((0, 0, 0))
            if not story.Story():
                running = False  # End story screen when out of images
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    return
            pg.display.update()
            clock.tick(60)  # Limit frame rate for smooth transitions
    
    def start():
        global boss_count
        running = True
        #시작 화면
        while running:
            screen.fill((0, 0, 0))  # 화면을 검정색으로 채움

            screen.blit(title_text, title_rect)
            screen.blit(start_text, start_rect)

            # 'Start' 버튼 클릭 감지
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if start_rect.collidepoint(event.pos):
                        story_screen()
                        #boss_count = True
                        stage1()
                        #stage1_boss()
                        running = False  # 'Start' 버튼 클릭 시 게임 시작

            pg.display.update()
    start()
    pg.quit()  # Pygame 종료


main()  # 게임 실행
