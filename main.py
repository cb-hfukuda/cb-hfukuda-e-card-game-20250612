import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 80, 80)
BLUE = (80, 160, 255)
CARD_WIDTH, CARD_HEIGHT = 100, 150

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Eカードゲーム - 奴隷側")

font = pygame.font.SysFont("meiryo", 28)
result_font = pygame.font.SysFont("meiryo", 44)
zawa_font = pygame.font.SysFont("meiryo", 36)

# 読み込みとサイズ調整
images = {
    "市民": pygame.image.load("citizen_card.png"),
    "奴隷": pygame.image.load("slave_card.png"),
    "王様": pygame.image.load("king_card.png")
}
for key in images:
    images[key] = pygame.transform.scale(images[key], (CARD_WIDTH, CARD_HEIGHT))

# 小型表示用（CPU残り手札）
small_images = {
    key: pygame.transform.scale(img, (40, 60)) for key, img in images.items()
}

initial_player_cards = ["市民1", "市民2", "奴隷", "市民3", "市民4"]
initial_cpu_cards = ["市民5", "市民6", "王様", "市民7", "市民8"]
player_cards = initial_player_cards.copy()
cpu_cards = initial_cpu_cards.copy()

step = 0
step_start_time = 0
selected_index = None
cpu_selected_index = None
cpu_card_pos = pygame.Rect(WIDTH // 2 - CARD_WIDTH // 2, HEIGHT // 2 - CARD_HEIGHT // 2 - 50, CARD_WIDTH, CARD_HEIGHT)

result_text = ""
result_color = WHITE
game_over = False

def judge(player, cpu):
    p = "市民" if "市民" in player else player
    c = "市民" if "市民" in cpu else cpu
    if p == "奴隷" and c == "王様":
        return "勝ち（逆転）！", RED
    elif p == "奴隷" and c == "市民":
        return "負け…", BLUE
    elif p == "市民" and c == "王様":
        return "負け…", BLUE
    elif p == "市民" and c == "市民":
        return "引き分け", WHITE
    return "？？？", WHITE

def draw_text_with_box(surface, text, font, color, center):
    text_surf = font.render(text, True, color)
    bg_rect = text_surf.get_rect(center=center)
    pygame.draw.rect(surface, BLACK, bg_rect.inflate(20, 20))
    surface.blit(text_surf, bg_rect)

clock = pygame.time.Clock()
running = True

while running:
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and step == 0 and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            for i, card in enumerate(player_cards):
                if card is not None:
                    rect = pygame.Rect(150 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 50, CARD_WIDTH, CARD_HEIGHT)
                    if rect.collidepoint(mouse_pos):
                        selected_index = i
                        cpu_choices = [j for j, c in enumerate(cpu_cards) if c is not None]
                        cpu_selected_index = random.choice(cpu_choices)
                        step = 1
                        step_start_time = now
                        result_text = ""
                        result_color = WHITE
                        game_over = False

        elif event.type == pygame.KEYDOWN and step == 2 and result_text == "引き分け":
            if event.key == pygame.K_r:
                player_cards[selected_index] = None
                cpu_cards[cpu_selected_index] = None
                step = 0
                step_start_time = 0
                selected_index = None
                cpu_selected_index = None
                result_text = ""
                result_color = WHITE
                game_over = False

        elif event.type == pygame.KEYDOWN and game_over and result_text != "引き分け":
            if event.key == pygame.K_r:
                player_cards = initial_player_cards.copy()
                cpu_cards = initial_cpu_cards.copy()
                step = 0
                step_start_time = 0
                selected_index = None
                cpu_selected_index = None
                result_text = ""
                result_color = WHITE
                game_over = False

    screen.fill(BLACK)

    # 残りカード表示
    remaining = sum(1 for c in player_cards if c is not None)
    remaining_text = font.render(f"残りカード：{remaining}枚", True, WHITE)
    screen.blit(remaining_text, (WIDTH - 250, 20))

    # プレイヤー手札
    for i, card in enumerate(player_cards):
        if card is not None:
            rect = pygame.Rect(150 + i * (CARD_WIDTH + 10), HEIGHT - CARD_HEIGHT - 50, CARD_WIDTH, CARD_HEIGHT)
            image = images["市民"] if "市民" in card else images[card]
            screen.blit(image, rect.topleft)

    # CPU手札（左上に小さく表示）
    for i, card in enumerate(cpu_cards):
        if card is not None:
            img = small_images["市民"] if "市民" in card else small_images[card]
            screen.blit(img, (20 + i * 70, 20))

    # ステップ描画
    if step == 1:
        elapsed = now - step_start_time
        text = ""
        if elapsed < 500:
            text = "ざわ・・・"
        elif elapsed < 1500:
            text = "ざわ・・・ ざわ・・・"
        elif elapsed < 2000:
            text = "ざわ・・・"
        elif elapsed < 3000:
            text = "ざわ・・・ ざわ・・・"
        elif elapsed < 4500:
            text = "CPUはこのカードを選んだ・・・"
        elif elapsed < 5000:
            image = images["市民"] if "市民" in cpu_cards[cpu_selected_index] else images[cpu_cards[cpu_selected_index]]
            screen.blit(image, cpu_card_pos.topleft)
        else:
            image = images["市民"] if "市民" in cpu_cards[cpu_selected_index] else images[cpu_cards[cpu_selected_index]]
            screen.blit(image, cpu_card_pos.topleft)
            if result_text == "":
                result_text, result_color = judge(player_cards[selected_index], cpu_cards[cpu_selected_index])
                if result_text != "引き分け":
                    player_cards[selected_index] = None
                    cpu_cards[cpu_selected_index] = None
                    game_over = True
                step = 2
                step_start_time = now
        if text:
            draw_text_with_box(screen, text, zawa_font, WHITE, (WIDTH // 2, HEIGHT // 2 - 150))

    elif step == 2:
        if cpu_selected_index is not None and cpu_cards[cpu_selected_index] is not None:
            image = images["市民"] if "市民" in cpu_cards[cpu_selected_index] else images[cpu_cards[cpu_selected_index]]
            screen.blit(image, cpu_card_pos.topleft)
        draw_text_with_box(screen, f"結果：{result_text}", result_font, result_color, (WIDTH // 2, HEIGHT // 2 - 100))
        if result_text == "引き分け":
            draw_text_with_box(screen, "Rキーで再戦", font, WHITE, (WIDTH // 2, HEIGHT // 2 - 40))
        else:
            draw_text_with_box(screen, "Rキーで最初から", font, WHITE, (WIDTH // 2, HEIGHT // 2 - 40))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
