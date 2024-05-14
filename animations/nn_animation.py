from manim import *
import numpy as np
import random
from manim_ml.neural_network.layers import FeedForwardLayer
from manim_ml.neural_network.neural_network import NeuralNetwork

def color_to_rgb_tuple(color):
    """Converts a Manim color object to an RGB tuple."""
    return tuple(np.round(color_to_rgb(color) * 255).astype(int))


def get_predicted_color_index(iteration: int, total_iterations:int, dot: Dot, colors: dict):
    """Returns the color corresponding to the given index."""
    
    # F1 score increases over time but starts at 30%
    f1_score = 0.33 + 0.67 * (iteration / total_iterations)


    result_correct = random.random() < f1_score
    if result_correct:
        predicted_color_index = list(colors.values()).index(str(dot.color.hex).upper())
    else:
        predicted_color_index = random.randint(0, 2)


    return predicted_color_index, f1_score




class NeuralNetworkAnimationFinal(Scene):

    def construct(self):
        # Define colors using RGB tuples for consistent comparison
        colors = {
            "Red": RED,
            "Blue": BLUE,
            "Green": GREEN
        }
       

        # Create input table with colored dots
        cols= 8
        rows = 3
        input_table = VGroup()
        for color in colors.values():
            for _ in range(cols):
                input_table.add(Dot(color=color, radius=0.12))
        input_table.arrange_in_grid(rows=rows, cols=cols, buff=0.2).to_edge(LEFT)
        
        # Define the neural network structure
        nn_structure = VGroup(
            Rectangle(width=2, height=1, color=ORANGE),
            Rectangle(width=2, height=1, color=BLUE),
            Rectangle(width=2, height=1, color=GREEN)
        ).arrange(DOWN, buff=0.5).to_edge(RIGHT)
        
        layers = [FeedForwardLayer(1), FeedForwardLayer(5), FeedForwardLayer(5), FeedForwardLayer(3)]
        nn = NeuralNetwork(layers)
        nn.scale(2)
        nn.move_to(ORIGIN)
        self.add(nn)
        training_dataset_text = Text("Prepared Training Dataset", font_size=24).move_to(input_table.get_center() + UP)
        self.add(training_dataset_text)
        self.add(input_table, nn_structure) 
        
        total_iterations = cols*rows
        # Animation loop
        f1_score_text = Text(f"f1_score: {33:.0f}%", font_size=30).to_edge(UP)
        self.add(f1_score_text)
        self.wait(1)
        
        for i in range(total_iterations):
            # Randomly select a dot to process
            dot = random.choice(input_table.submobjects)
            input_table.remove(dot)
            

            self.play(dot.animate.move_to(nn[0].get_left()+RIGHT*.3))
            self.play(FadeOut(dot))
            
            forward_propagation_animation= nn.make_forward_pass_animation(
                run_time=1, passing_flash=True
            )
            self.play(forward_propagation_animation, run_time=1)
            
            predicted_color_index, f1_score = get_predicted_color_index(i, total_iterations, dot, colors)
            # display confidence as a text (%) increase over time:
            node_spacing=0.6
            dot_down_multiplier = node_spacing * predicted_color_index
            dot.move_to(nn[0].get_right()-LEFT*.3+DOWN*dot_down_multiplier+node_spacing*UP)

            self.play(dot.animate.move_to(nn_structure[predicted_color_index].get_center()),
                      Transform(f1_score_text, Text(f"f1_score: {f1_score*100:.0f}%", font_size=30).to_edge(UP)))

            self.play(FadeOut(dot))
            
        input_table = VGroup()
        production_data_dots_count = 10
        for _ in range(production_data_dots_count):
            input_table.add(Dot(color=WHITE))
        input_table.arrange_in_grid(rows=1, cols=10, buff=0.2).to_edge(LEFT)
        self.play(Transform(training_dataset_text, Text("Production Data", font_size=24).move_to(input_table.get_center() + UP)))
        self.add(input_table)

       
        for _ in range(production_data_dots_count):

            dot = random.choice(input_table.submobjects)
            input_table.remove(dot)
            

            self.play(dot.animate.move_to(nn[0].get_left()+RIGHT*.5))
            self.play(FadeOut(dot))
            
            
            forward_propagation_animation= nn.make_forward_pass_animation(
                run_time=1, passing_flash=True
            )
            self.play(forward_propagation_animation, run_time=1)
            
            #predicted_color_index, f1_score = get_predicted_color_index(i, total_iterations, dot, colors)
            # display confidence as a text (%) increase over time:
            predicted_color_index = random.randint(0, 2)
            node_spacing=0.6
            dot_down_multiplier = node_spacing * predicted_color_index
            dot.move_to(nn[0].get_right()-LEFT*.3+DOWN*dot_down_multiplier+node_spacing*UP)
            
            self.play(dot.animate.move_to(nn_structure[predicted_color_index].get_center())
                        )
            self.play(FadeOut(dot))


            """
            dot = random.choice(input_table.submobjects)
            predicted_color_index = random.randint(0, 2)
            input_table.remove(dot)
            # change color of the dot to the predicted color
            
            self.play(dot.animate.move_to(nn_structure[predicted_color_index].get_center())
                        )
            dot.set_color(colors[list(colors.keys())[predicted_color_index]])
            self.play(FadeOut(dot))"""

        self.wait(1)

if __name__ == "__main__":
    scene = NeuralNetworkAnimationFinal()
    scene.render()
