import numpy as np
import time
import os

# Initialize rotation angles
A, B, C = 0.0, 0.0, 0.0

# Constants
width = 144
height = 60
bg_ascii = ' '
K1 = 40.0
increment_speed = 0.6

cube_width = 20.0
horizontal_offset = -2 * cube_width

# Buffers
z_buffer = np.zeros((width * height), dtype=float)
buffer = np.full((width * height), bg_ascii, dtype=str)

def get_rotation_matrix():
    # Rotation around X-axis
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(A), -np.sin(A)],
        [0, np.sin(A), np.cos(A)]
    ])
    
    # Rotation around Y-axis
    Ry = np.array([
        [np.cos(B), 0, np.sin(B)],
        [0, 1, 0],
        [-np.sin(B), 0, np.cos(B)]
    ])
    
    # Rotation around Z-axis
    Rz = np.array([
        [np.cos(C), -np.sin(C), 0],
        [np.sin(C), np.cos(C), 0],
        [0, 0, 1]
    ])
    
    # Combined rotation matrix
    return Rz @ Ry @ Rx

def calculate_plane(cube_x, cube_y, cube_z, ch):
    global z_buffer, buffer
    
    # Create point and apply rotation
    point = np.array([cube_x, cube_y, cube_z])
    R = get_rotation_matrix()
    rotated = R @ point
    
    x, y, z = rotated[0], rotated[1], rotated[2] + 100.0  # Adding distance from camera
    
    ooz = 1.0 / z if z != 0 else 0
    
    # Calculate projected x and y
    xp = int(width // 2 + horizontal_offset + K1 * ooz * x * 2)
    yp = int(height // 2 + K1 * ooz * y)
    
    idx = xp + yp * width
    if 0 <= idx < width * height:
        if ooz > z_buffer[idx]:
            z_buffer[idx] = ooz
            buffer[idx] = ch

def main():
    global A, B, C
    
    # Clear screen
    os.system('cls' if os.name == 'nt' else 'clear')
    
    while True:
        # Reset buffers
        buffer.fill(bg_ascii)
        z_buffer.fill(0)
        
        # Calculate cube faces
        for cube_x in np.arange(-cube_width, cube_width, increment_speed):
            for cube_y in np.arange(-cube_width, cube_width, increment_speed):
                calculate_plane(cube_x, cube_y, -cube_width, '@')  # Front face
                calculate_plane(cube_width, cube_y, cube_x, '$')   # Right face
                calculate_plane(-cube_width, cube_y, -cube_x, '~') # Left face
                calculate_plane(-cube_x, cube_y, cube_width, '#')  # Back face
                calculate_plane(cube_x, -cube_width, -cube_y, ';') # Bottom face
                calculate_plane(cube_x, cube_width, cube_y, '+')   # Top face
        
        # Move cursor to home position
        print("\033[H", end="")
        
        # Print the frame
        for k in range(width * height):
            print(buffer[k], end=('\n' if (k + 1) % width == 0 else ''))
        
        # Update rotation angles
        A += 0.05
        B += 0.05
        C += 0.01
        
        # Delay for ~60 FPS
        time.sleep(0.016)

if __name__ == "__main__":
    main() 