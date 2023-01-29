import pygame, requests, sys, os
 
# Создайте оконное приложение, отображающее карту по координатам и в масштабе, который задаётся программно.
 
class MapParams(object):
    def __init__(self):
        self.lat = 55.833980  # Координаты центра карты на старте. Задал координаты университета 55.833980, 37.543506
        self.lon = 37.543506
        self.zoom = 15  # Масштаб карты на старте. Изменяется от 1 до 19
        self.type = "map" # Другие значения "sat", "sat,skl"
 
    # Преобразование координат в параметр ll, требуется без пробелов, через запятую и без скобок
    def ll(self):
        return str(self.lon)+","+str(self.lat)
 
# Создание карты с соответствующими параметрами.
def load_map(mp):
    map_request = "http://static-maps.yandex.ru/1.x/?ll={ll}&z={z}&l={type}".format(ll=mp.ll(), z=mp.zoom, type=mp.type)
    response = requests.get(map_request)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)
 
    # Запись полученного изображения в файл.
    map_file = "map.png"
    try:
        with open(map_file, "wb") as file:
            file.write(response.content)
    except IOError as ex:
        print("Ошибка записи временного файла:", ex)
        sys.exit(2)
    return map_file
         
def main():
    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 550))
    screen.fill((255, 255, 255))
    mp = MapParams()
    
    base_font = pygame.font.Font(None, 32)
    user_text = ''
    
    # create rectangle 
    input_rect = pygame.Rect(225, 500, 140, 32)
    
    # color_active stores color(lightskyblue3) which
    # gets active when input box is clicked by user
    color_active = pygame.Color('lightskyblue3')
    
    # color_passive store color(chartreuse4) which is
    # color of input box.
    color_passive = pygame.Color('chartreuse4')
    color = color_passive
    
    active = False
  
    while True:
        for event in pygame.event.get():
    
        # if user types QUIT then the screen will close
            if event.type == pygame.QUIT:
                pygame.quit()
                os.remove(map_file)
                sys.exit()
    
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
    
            if event.type == pygame.KEYDOWN:
    
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
    
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
    
                # Unicode standard is used for string
                # formation
                else:
                    user_text += event.unicode
        #Создаем файл
        map_file = load_map(mp)
        if active:
            color = color_active
        else:
            color = color_passive
            
        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)
    
        text_surface = base_font.render(user_text, True, (255, 255, 255))
        
        # render at position stated in arguments
        screen.blit(text_surface, (input_rect.x+5, input_rect.y+5))
        
        # set width of textfield so that text cannot get
        # outside of user's text input
        input_rect.w = max(100, text_surface.get_width()+10)
        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        pygame.display.flip()
   
if __name__ == "__main__":
    main()
