import rasterio
import numpy as np
import os
import csv
from rasterio.warp import calculate_default_transform, reproject, Resampling

# Paths de los archivos raster
raster_real_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Rasteriza_lul_igm\rasterizado_lulc_igm_actual.tif"
raster_pred_path = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Clasifica_RF_CART_SVM\Raster_Results\LULC_2009_2015_RF.tif"
output_dir = r"C:\Users\gisse\OneDrive\Escritorio\Repositorio\Documentos\Clasifica_GEE\Matriz_confusion"

# Cambiar la proyección de un raster
def reproject_raster(input_path, output_path, dst_crs):
    with rasterio.open(input_path) as src:
        transform, width, height = calculate_default_transform(
            src.crs, dst_crs, src.width, src.height, *src.bounds
        )
        meta = src.meta.copy()
        meta.update({"crs": dst_crs, "transform": transform, "width": width, "height": height})

        with rasterio.open(output_path, "w", **meta) as dest:
            for i in range(1, src.count + 1):
                reproject(
                    source=rasterio.band(src, i),
                    destination=rasterio.band(dest, i),
                    src_transform=src.transform,
                    src_crs=src.crs,
                    dst_transform=transform,
                    dst_crs=dst_crs,
                    resampling=Resampling.nearest,
                )

# Calcular métricas de clasificación
def calculate_metrics(real_data, pred_data):
    metrics = {}
    total_tp = total_fn = total_fp = total_tn = 0
    classes = range(1, 11)  # Clases de 1 a 10

    for cls in classes:
        tp = np.sum((real_data == cls) & (pred_data == cls))
        fn = np.sum((real_data == cls) & (pred_data != cls))
        fp = np.sum((real_data != cls) & (pred_data == cls))
        tn = np.sum((real_data != cls) & (pred_data != cls))

        metrics[cls] = {"TP": tp, "FN": fn, "FP": fp, "TN": tn}
        total_tp += tp
        total_fn += fn
        total_fp += fp
        total_tn += tn

    total_metrics = {
        "TP": total_tp,
        "FN": total_fn,
        "FP": total_fp,
        "TN": total_tn,
        "P": total_tp + total_fn,
        "N": total_fp + total_tn,
    }
    return metrics, total_metrics

# Calcular métricas derivadas
def calculate_derived_metrics(total_metrics):
    TP, FN, FP, TN, P, N = total_metrics["TP"], total_metrics["FN"], total_metrics["FP"], total_metrics["TN"], total_metrics["P"], total_metrics["N"]
    recall = TP / P if P > 0 else 0
    tn_rate = TN / N if N > 0 else 0
    accuracy = (TP + TN) / (P + N) if (P + N) > 0 else 0
    error_rate = 1 - accuracy
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    f_measure = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "Recall (TP Rate)": recall,
        "TN Rate": tn_rate,
        "Accuracy": accuracy,
        "Error Rate": error_rate,
        "Precision": precision,
        "F Measure": f_measure,
    }

# Guardar métricas en CSV
def save_metrics_to_csv(metrics, derived_metrics, output_path):
    with open(output_path, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Class", "TP", "FN", "FP", "TN"])
        for cls, values in metrics.items():
            writer.writerow([cls, values["TP"], values["FN"], values["FP"], values["TN"]])
        
        writer.writerow([])
        writer.writerow(["Metric", "Value"])
        for key, value in derived_metrics.items():
            writer.writerow([key, value])

# Proceso principal
try:
    # Cargar raster real
    with rasterio.open(raster_real_path) as real_src:
        real_data = real_src.read(1)
       # real_crs = real_src.crs

    # Cargar raster predicho 
    with rasterio.open(raster_pred_path) as pred_src:
        pred_data = pred_src.read(1)
        #pred_crs = pred_src.crs

    # Calcular métricas
    metrics, total_metrics = calculate_metrics(real_data, pred_data)
    derived_metrics = calculate_derived_metrics(total_metrics)

    # Guardar métricas en CSV
    metrics_csv_path = os.path.join(output_dir, "classification_metrics_RF.csv")
    save_metrics_to_csv(metrics, derived_metrics, metrics_csv_path)

    print("Métricas guardadas en:")
    print(metrics_csv_path)

except Exception as e:
    print(f"Error: {e}")
    
