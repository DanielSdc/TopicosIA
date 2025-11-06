import os
import numpy as np
import matplotlib.pyplot as plt
import imageio

# Limpia frames previos en el directorio dado para no unificar anteriores con la nueva ejecución
def limpiar_frames(frames_dir):
   if os.path.exists(frames_dir):
        old_frames = sorted([
            os.path.join(frames_dir, f)
            for f in os.listdir(frames_dir)
            if f.startswith("frame_") and f.endswith(".png")
        ])
        deleted_prev = 0
        for p in old_frames:
            try:
                os.remove(p)
                deleted_prev += 1
            except Exception:
                pass
        if deleted_prev:
            print(f"Eliminados {deleted_prev} frames de ejecuciones previas.")

# Guardar un frame de la iteración actual
# Se guarda un frame cada 'frame_every' iteraciones en la ruta 'frames_dir'
def guardar_frame(optimizador, frames_dir, it, dimensiones, global_best_pos, pos_it, costo_it, frame_every, saved_frames, df):
    try:
            fig, ax = plt.subplots(figsize=(6, 5))
            # cultivos
            ax.scatter(df["Longitud"], df["Latitud"], c="gray", s=30, alpha=0.6)

            # todas las partículas actuales (cada partícula tiene S sensores)
            try:
                particles = optimizador.swarm.position  # (n_particles, dimensions)
                cmap = plt.get_cmap("tab10")
                # Número de sensores por partícula (dimensiones / 2)
                n_sensors = dimensiones // 2 if dimensiones >= 2 else 1
                # Para cada índice de sensor s, dibujar la posición de ese sensor
                # para todas las partículas con el mismo color.
                for s in range(n_sensors):
                    xs = particles[:, s * 2 + 1]
                    ys = particles[:, s * 2]
                    color = cmap(s % cmap.N)
                    ax.scatter(xs, ys, c=[color], s=30, alpha=0.6, marker='o')
            except Exception:
                pass
            # mejor solución hasta ahora
            best_to_plot = global_best_pos if global_best_pos is not None else pos_it
            sensores_best = np.asarray(best_to_plot).reshape(-1, 2)
            ax.scatter(sensores_best[:,1], sensores_best[:,0], c="red", marker="x", s=90, label="Mejor")

            ax.set_xlabel("Longitud")
            ax.set_ylabel("Latitud")
            ax.set_title(f"Iter {it}: Mejor costo {costo_it:.2f}")
            ax.grid(alpha=0.3)
            plt.tight_layout()
            # Guardar solo cada frame_every iteraciones
            if it % frame_every == 0:
                frame_path = os.path.join(frames_dir, f"frame_{it:04d}.png")
                fig.savefig(frame_path, dpi=120)
                saved_frames.append(frame_path)
            plt.close(fig)
    except Exception:
            pass            
    
# Generar un plot con cultivos y sensores (mejor solucion)  
# Se guarda en la ruta 'base' un plot con la mejor solución encontrada  
def plot_mejor_solucion (df, mejor_pos, base):
    print("Generando plot de la mejor solucion encontrada...") 
    plt.figure(figsize=(8, 6))
    plt.scatter(df["Longitud"], df["Latitud"], c="gray", s=40, alpha=0.6, label="Cultivos")
    sensores = np.asarray(mejor_pos).reshape(-1, 2)
    # sensors[:,0]=lat, sensors[:,1]=lon
    plt.scatter(sensores[:,1], sensores[:,0], c="red", marker="x", s=100, label="Sensores (mejor)")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.title("Mejor solucion: sensores vs cultivos")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plot_path = os.path.join(base, "best_solution_plot.png")
    plt.savefig(plot_path, dpi=150)
    plt.close()
    print(f"Plot guardado en: {plot_path}")

# Combinar frames en un GIF animado
# Se guarda un GIF mostrando la evolución de la optimizacion en la ruta 'base'
def crear_gif_iteraciones (frames_dir, base):
    
    print("Creando GIF de la evolucion de la optimizacion...")
    frames_list = sorted(
        [os.path.join(frames_dir, f) for f in os.listdir(frames_dir) if f.startswith("frame_") and f.endswith(".png")]
    )
    if frames_list:
        images = [imageio.v2.imread(p) for p in frames_list]
        try:
            gif_path = os.path.join(base, "evolution.gif")
            imageio.mimsave(gif_path, images, duration=0.2)
            print(f"GIF de evolucion guardado en: {gif_path}")
        except Exception as e:
            print("No se pudo crear el GIF:", e)

        print(f"Frames temporales conservados en: {frames_dir} (se eliminaran al iniciar la proxima ejecucion).")
    else:
        print("No se encontraron frames para crear GIF.")


# Función para guardar el frame de evolución del costo
# Se guarda un frame cada 'frame_every' iteraciones en la ruta 'base'
def guardar_frame_costo(best_costs, base, it, frame_every, saved_frames_cost):

    if it % frame_every == 0:
        fig, ax = plt.subplots(figsize=(6, 4))
        iters = list(range(1, len(best_costs) + 1))
        # Dibujar la curva como línea continua (sin marcadores) y un poco más gruesa
        ax.plot(iters, best_costs, marker=None, linestyle="-", color="C1", linewidth=2)
        ax.set_xlabel("Iteración")
        ax.set_ylabel("Mejor costo")
        ax.set_title(f"Evolución del mejor costo ({it} iteraciones)")
        ax.grid(alpha=0.3)
        plt.tight_layout()
        frame_path = os.path.join(base, f"frame_evolution_cost.png")
        fig.savefig(frame_path, dpi=120)
        saved_frames_cost.append(frame_path)
        plt.close(fig)