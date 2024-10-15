import cv2 as cv
import time
import tkinter as tk
from tkinter import ttk
from threading import Thread
from hand_estimation import HandTrackingDynamic

class CookingAssistantApp:
    def __init__(self, root):
        self.recipes = """Recipe: The Ultimate Pancakes
1. Mix flour, milk, eggs, and sugar thoroughly until smooth.
2. Let the batter rest for 15 minutes.
3. Pour batter into a hot pan and cook on medium heat.
4. Cook until bubbles form on the surface, then flip.
5. Continue cooking until golden brown on both sides.
6. Serve with your favorite toppings like syrup, berries, or whipped cream.

Recipe: Spaghetti Bolognese
1. Boil water in a pot and add a pinch of salt.
2. Cook spaghetti according to package instructions until al dente.
3. Meanwhile, heat oil in a skillet and sauté chopped onions and garlic until translucent.
4. Add minced meat, breaking it apart while cooking until browned.
5. Add tomato sauce, salt, pepper, and herbs to the skillet.
6. Simmer the sauce for 20 minutes, stirring occasionally.
7. Serve the Bolognese sauce over spaghetti and garnish with grated cheese.

Recipe: Fresh Garden Salad
1. Chop lettuce, cucumber, and tomatoes into bite-sized pieces.
2. Slice red onions thinly and add them to the salad.
3. Add croutons and sprinkle with shredded cheese.
4. Drizzle your favorite dressing over the salad and mix well.
5. Serve immediately for a fresh and crisp experience.

Recipe: Chicken Stir Fry
1. Cut chicken breast into thin strips.
2. Heat a tablespoon of oil in a wok or skillet.
3. Add chicken strips and stir-fry until cooked through.
4. Add sliced bell peppers, broccoli florets, and snap peas.
5. Stir-fry vegetables until tender yet crisp.
6. Add soy sauce and a bit of honey for flavor.
7. Serve with steamed rice.

Recipe: Chocolate Chip Cookies
1. Preheat oven to 350°F (175°C).
2. In a bowl, cream together butter and sugar.
3. Add eggs and vanilla extract, beating until smooth.
4. Stir in flour, baking soda, and salt.
5. Fold in chocolate chips.
6. Drop spoonfuls of dough onto a baking sheet.
7. Bake for 10-12 minutes or until edges are golden brown.

Recipe: Smoothie Bowl
1. Blend frozen bananas, berries, and a splash of almond milk until smooth.
2. Pour the smoothie into a bowl.
3. Top with granola, sliced fruit, and a drizzle of honey.
4. Enjoy as a refreshing breakfast or snack."""
        self.current_recipe_index = 0
        self.root = root
        self.root.title("Cooking Assistant")
        self.root.geometry("1000x600")
        self.root.configure(bg='white')
        
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Grid layout for buttons, video, and recipe
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        self.start_button = ttk.Button(self.button_frame, text="Start Hand Tracking", command=self.start_hand_tracking)
        self.start_button.grid(row=0, column=0, padx=5, pady=5)

        self.stop_button = ttk.Button(self.button_frame, text="Stop Hand Tracking", command=self.stop_hand_tracking)
        self.stop_button.grid(row=1, column=0, padx=5, pady=5)

        self.video_label = ttk.Label(self.main_frame)
        self.video_label.grid(row=1, column=0, padx=10, pady=10)

        self.recipe_label = tk.Text(self.main_frame, wrap='word', width=50, height=30, font=('Helvetica', 32))
        self.recipe_label.insert('1.0', self.recipes)
        self.recipe_label.config(state='disabled')
        self.recipe_label.grid(row=0, column=1, rowspan=2, padx=10, pady=10, sticky='n')

        self.cap = None
        self.running = False

    def start_hand_tracking(self):
        if not self.running:
            self.running = True
            self.cap = cv.VideoCapture(0)
            self.cap.set(cv.CAP_PROP_FRAME_WIDTH, 640)
            self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, 480)
            if not self.cap.isOpened():
                print("Cannot open camera")
                return
            self.detector = HandTrackingDynamic()
            Thread(target=self.hand_tracking_loop, daemon=True).start()

    def stop_hand_tracking(self):
        self.running = False
        if self.cap:
            self.cap.release()
        self.video_label.config(image='')
        self.cap.release()
        cv.destroyAllWindows()

    def hand_tracking_loop(self):
        ptime = 0
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            frame = self.detector.findFingers(frame)
            lmsList, bbox = self.detector.findPosition(frame)

            if len(lmsList) != 0:
                fingers = self.detector.findFingerUp()
                # Scroll down if index finger is up
                if fingers[1] == 1 and sum(fingers) == 1:
                    self.recipe_label.config(state='normal')
                    self.recipe_label.yview_scroll(1, 'units')
                    self.recipe_label.config(state='disabled')
                # Scroll up if thumb is up
                elif fingers[0] == 1 and sum(fingers) == 1:
                    self.recipe_label.config(state='normal')
                    self.recipe_label.yview_scroll(-1, 'units')
                    self.recipe_label.config(state='disabled')

            ctime = time.time()
            fps = 1 / (ctime - ptime)
            ptime = ctime

            cv.putText(frame, f'FPS: {int(fps)}', (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 0, 255), 3)
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            img = cv.resize(img, (640, 480))
            self.update_video_label(img)

    def update_video_label(self, img):
        from PIL import Image, ImageTk
        image = Image.fromarray(img)
        imgtk = ImageTk.PhotoImage(image=image)
        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

if __name__ == "__main__":
    root = tk.Tk()
    app = CookingAssistantApp(root)
    root.mainloop()