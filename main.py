import pygame,sys
from game import Game
from colors import Colors
import time

pygame.init()

title_font = pygame.font.Font(None, 40)
score_surface = title_font.render("Score", True, Colors.white)
next_surface = title_font.render("Next", True, Colors.white)
game_over_surface = title_font.render("GAME OVER", True, Colors.white)

score_rect = pygame.Rect(320, 55, 170, 60)
next_rect = pygame.Rect(320, 215, 170, 180)

screen = pygame.display.set_mode((500, 620))
pygame.display.set_caption("Python Tetris") #Tiêu đề của game

clock = pygame.time.Clock()
game_state = "menu"
game = Game()

GAME_UPDATE = pygame.USEREVENT
pygame.time.set_timer(GAME_UPDATE, 200) #Bien toc do roi

start_time = time.time()


def show_start_screen():
	screen.fill(Colors.dark_blue)
	title_font = pygame.font.Font(None, 60)
	start_surface = title_font.render("Python Tetris", True, Colors.white)
	start_rect = start_surface.get_rect(center=(250, 200))
	start_button = pygame.Rect(150, 300, 200, 50)

	pygame.draw.rect(screen, Colors.light_blue, start_button)
	start_text = title_font.render("Start", True, Colors.dark_blue)
	start_text_rect = start_text.get_rect(center=start_button.center)

	screen.blit(start_surface, start_rect)
	screen.blit(start_text, start_text_rect)

	pygame.display.update()

	# Lặp qua sự kiện và chờ người dùng nhấn nút Start
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if start_button.collidepoint(event.pos):
					waiting = False


def show_game_over_screen():
	global game_state
	screen.fill(Colors.dark_blue)
	title_font = pygame.font.Font(None, 60)
	game_over_surface = title_font.render("Game Over", True, Colors.white)
	game_over_rect = game_over_surface.get_rect(center=(250, 200))
	restart_button = pygame.Rect(150, 300, 200, 50)
	exit_button = pygame.Rect(150, 350, 100, 50)

	pygame.draw.rect(screen, Colors.light_blue, restart_button)
	pygame.draw.rect(screen, Colors.light_blue, exit_button)

	restart_text = title_font.render("Restart", True, Colors.dark_blue)
	exit_text = title_font.render("Exit", True, Colors.white)

	screen.blit(game_over_surface, game_over_rect)
	screen.blit(restart_text, restart_text.get_rect(center=restart_button.center))
	screen.blit(exit_text, exit_text.get_rect(center=exit_button.center))

	pygame.display.update()

	# Lặp qua sự kiện và chờ người dùng nhấn nút Restart hoặc Exit
	waiting = True
	while waiting:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if restart_button.collidepoint(event.pos):
					game.reset()
					game_state = "game"
					waiting = False

				elif exit_button.collidepoint(event.pos):
					pygame.quit()
					sys.exit()
	# pygame.display.update()

while True:
	keys = pygame.key.get_pressed()
	if game_state == "menu":
		show_start_screen()
		game_state = "game"

	if game_state == "game":

		current_time = time.time()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if game.game_over == True:
					# game.game_over = False
					game_state = "game_over"
					# game.reset()

				if event.key == pygame.K_LEFT and game.game_over == False:
					game.move_left()
				if event.key == pygame.K_RIGHT and game.game_over == False:
					game.move_right()
				if event.key == pygame.K_DOWN and game.game_over == False:
					game.move_down()
					game.update_score(0, 1)
				if event.key == pygame.K_UP and game.game_over == False:
					game.rotate()
			if keys[pygame.K_DOWN] and game.game_over == False:
				game.move_down()
				game.update_score(0, 1)

			if event.type == GAME_UPDATE and game.game_over == False:
				game.move_down()  #các khối di chuyển xuống

			if game.game_over:
				game_state = "game_over"
				#Source thay xoay các khối sau 2 giây
				# if current_time - start_time >= 2:
				# 	# Sau 2 giây, đặt lại thời gian bắt đầu
				# 	start_time = current_time
				# 	game.rotate()


	if game_state == "game_over":
		show_game_over_screen()
		print("game over")
		# break
		#lỗi chô này
		# game_state = "menu"


	#Drawing
	score_value_surface = title_font.render(str(game.score), True, Colors.white)

	screen.fill(Colors.dark_blue)
	screen.blit(score_surface, (365, 20, 50, 50))
	screen.blit(next_surface, (375, 180, 50, 50))

	if game.game_over == True:
		screen.blit(game_over_surface, (320, 450, 50, 50))

	pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
	screen.blit(score_value_surface, score_value_surface.get_rect(centerx = score_rect.centerx,
		centery = score_rect.centery))
	pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)
	game.draw(screen)

	pygame.display.update()
	clock.tick(60)