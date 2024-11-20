class LastBoss(Character):
    def __init__(self, x, y):
        super().__init__(os.path.join(image_path, "원장1.png"), x, y, 0.05, 200)
        self.hp = 200
        self.red_zones = []  # 빨간 판 정보 리스트
        self.lightning_image = pg.image.load(os.path.join(image_path, "벼락.png"))  # 벼락 이미지
        self.red_zone_image = pg.Surface((100, 100), pg.SRCALPHA)  # 빨간 판 이미지
        pg.draw.rect(self.red_zone_image, (255, 0, 0, 128), self.red_zone_image.get_rect())  # 반투명 빨간 판
        self.last_zone_time = 0
        self.zone_interval = 2000  # 빨간 판 생성 간격 (2초)

        # 빨간 판 생성
        current_time = pg.time.get_ticks()
        if current_time - self.last_zone_time >= self.zone_interval:
            self.create_red_zone()
            self.last_zone_time = current_time

        # 빨간 판과 벼락 업데이트
        for zone in self.red_zones[:]:
            zone["timer"] -= dt
            if zone["timer"] <= 0:
                # 벼락 생성 후 빨간 판 제거
                self.drop_lightning(zone["pos"], ethan)
                self.red_zones.remove(zone)

    def create_red_zone(self):
        # 화면 내 랜덤 위치에 빨간 판 생성
        x = random.randint(50, screen_width - 150)
        y = random.randint(50, screen_height - 150)
        self.red_zones.append({"pos": (x, y), "timer": 1000})  # 1초 타이머와 위치 저장

    def drop_lightning(self, position, ethan):
        # 벼락 생성 애니메이션 및 충돌 처리
        lightning_rect = self.lightning_image.get_rect(center=position)
        screen.blit(self.lightning_image, lightning_rect)

        if ethan.rect.colliderect(lightning_rect):  # 벼락과 에단 충돌 시
            ethan.hit()


    def draw(self):
        # 보스 그리기
        super().draw()

        # 빨간 판 그리기
        for zone in self.red_zones:
            screen.blit(self.red_zone_image, zone["pos"])


def boss():
    
    lastboss = LastBoss(screen_width // 2, 0)
    running = True

    while running:
        dt = clock.tick(60)
        screen.blit(pg.image.load(os.path.join(image_path, "보스2페이지.png")), (0, 0))  # 새로운 배경 이미지

        # 이벤트 처리
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_w:
                    ethan.shoot((0, -1), 90)
                elif event.key == pg.K_s:
                    ethan.shoot((0, 1), 270)
                elif event.key == pg.K_a:
                    ethan.shoot((-1, 0), 180)
                elif event.key == pg.K_d:
                    ethan.shoot((1, 0), 0)

        # 에단 이동
        keys = pg.key.get_pressed()
        ethan.move(keys[pg.K_RIGHT] - keys[pg.K_LEFT], keys[pg.K_DOWN] - keys[pg.K_UP], dt)

        # 보스 업데이트
        if lastboss.hp > 0:
            lastboss.update(dt, ethan)
            lastboss.draw()
            # 보스 체력 표시
            hp_bar_width = 300 * (lastboss.hp / 50)
            pg.draw.rect(screen, (100, 100, 100), ((screen_width - 300) / 2, 30, 300, 20))  # 배경 바
            pg.draw.rect(screen, (255, 0, 0), ((screen_width - 300) / 2, 30, hp_bar_width, 20))  # 체력 바

        # 에단과 그리기
        ethan.draw()
        

        # 에단 체력 그리기
        ethan.draw_lives(screen)

        # 보스 죽음 처리
        if lastboss.hp <= 0:
            ending()
            running = False  # 보스가 죽으면 종료

        # 에단 죽음 처리
        if ethan.lives <= 0:
            retry()
            running = False  # 에단이 죽으면 종료

        pg.display.update()
