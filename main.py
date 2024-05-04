

import pygame, sys
from button import Button
from game import Game
from colors import Colors
import time
from datetime import timedelta

pygame.init()
SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("assets/Background.png")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def options():
	while True:
		OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

		SCREEN.fill("white")

		OPTIONS_TEXT = get_font(45).render("This is the OPTIONS screen.", True, "Black")
		OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
		SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

		OPTIONS_BACK = Button(image=None, pos=(640, 460),
							  text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

		OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
		OPTIONS_BACK.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
					main_menu()

		pygame.display.update()

def main_menu():
	SCREEN = pygame.display.set_mode((1280, 720))
	while True:
		SCREEN.blit(BG, (0, 0))

		MENU_MOUSE_POS = pygame.mouse.get_pos()

		MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
		MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

		PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250),
							 text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		# OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400),
		# 						text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
		QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 400),
							 text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

		SCREEN.blit(MENU_TEXT, MENU_RECT)

		# for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
		# 	button.changeColor(MENU_MOUSE_POS)
		# 	button.update(SCREEN)

		for button in [PLAY_BUTTON, QUIT_BUTTON]:
			button.changeColor(MENU_MOUSE_POS)
			button.update(SCREEN)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.MOUSEBUTTONDOWN:
				if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
					play()
				# if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
				# 	options()
				if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
					pygame.quit()
					sys.exit()
		pygame.display.update()


def play():
	SCREEN.fill("black")
	title_font = pygame.font.Font(None, 40)
	score_surface = title_font.render("Score", True, Colors.white)
	next_surface = title_font.render("Next", True, Colors.white)
	game_over_surface = title_font.render("GAME OVER", True, Colors.white)
	time_surface = title_font.render("Time", True, Colors.white)
	game_restart = title_font.render("RESTART", True, Colors.orange)
	game_back = title_font.render("BACK", True, Colors.yellow)
	game_quit = title_font.render("QUIT", True, Colors.red)

	score_rect = pygame.Rect(320, 55, 170, 60)
	next_rect = pygame.Rect(320, 215, 170, 180)
	time_rect = pygame.Rect(320, 440, 170, 170)

	screen = pygame.display.set_mode((500, 620))

	pygame.display.set_caption("Python Tetris")  # Tiêu đề của game

	clock = pygame.time.Clock()

	game = Game()

	GAME_UPDATE = pygame.USEREVENT
	pygame.time.set_timer(GAME_UPDATE, 200)  # Bien toc do roi



	start_time = time.time()

	while True:
		keys = pygame.key.get_pressed()
		current_time = time.time()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				# if game.game_over == True :
				# 	game.game_over = False
				# 	game.reset()
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
				game.move_down()  # các khối di chuyển xuống

		#Source thay xoay các khối sau 2 giây
		if current_time - start_time >= 1:
			# Sau 2 giây, đặt lại thời gian bắt đầu
			start_time = current_time
			game.rotate()

		# Drawing
		score_value_surface = title_font.render(str(game.score), True, Colors.white)

		screen.fill(Colors.dark_blue)
		screen.blit(score_surface, (365, 20, 50, 50))
		screen.blit(next_surface, (375, 180, 50, 50))


		if game.game_over == True:
			pygame.draw.rect(screen, Colors.light_blue, time_rect, 0, 10)
			screen.blit(game_over_surface, (320, 500, 50, 50))
			screen.blit(game_restart, (320, 535, 50, 50))
			screen.blit(game_back, (320, 560, 50, 50))
			screen.blit(game_quit, (415, 560, 50, 50))

			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_x, mouse_y = event.pos
				print(mouse_x, mouse_y)
				#restart
				if 322 <= mouse_x <= 440 and 536 <= mouse_y <= 557:
					game.game_over = False
					game.reset()

				#back
				if 326 <= mouse_x <= 397 and 563 <= mouse_y <= 581:
					game.game_over = False
					game.reset()
					main_menu()
					print("back")
				#quit
				if 423 <= mouse_x <= 480 and 566 <= mouse_y <= 579:
					game.game_over = False
					game.reset()
					pygame.quit()
					print("quit")

		else:
			game.update_timer()
			pygame.draw.rect(screen, Colors.light_blue, time_rect, 0, 10)
			time_remaining_surface = title_font.render(str(timedelta(seconds=max(int(game.countdown_time), 0))),
													   True, Colors.white)
			screen.blit(time_remaining_surface, (360, 500, 50, 50))
			screen.blit(time_surface, (375, 450, 50, 50))


		pygame.draw.rect(screen, Colors.light_blue, score_rect, 0, 10)
		screen.blit(score_value_surface, score_value_surface.get_rect(centerx=score_rect.centerx,centery=score_rect.centery))

		pygame.draw.rect(screen, Colors.light_blue, next_rect, 0, 10)

		game.draw(screen)

		pygame.display.update()
		clock.tick(60)

main_menu()