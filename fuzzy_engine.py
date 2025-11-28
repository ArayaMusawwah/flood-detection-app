import numpy as np
from typing import Dict, List, Tuple, Optional, Any

class FuzzyFloodEngine:
    """
    Engine Fuzzy Logic untuk deteksi banjir.
    Menggunakan metode Mamdani dengan fungsi keanggotaan Trapesium.
    """

    def __init__(self):
        # Input MFs Parameters
        self.CR_params = {
            "rendah": [0, 0, 50, 100],
            "sedang": [50, 100, 150, 200],
            "tinggi": [150, 200, 300, 300]
        }

        self.WL_params = {
            "rendah": [0, 0, 1, 2],
            "sedang": [1.5, 2.5, 3.1, 5],
            "tinggi": [2.5, 3.1, 5, 5]
        }

        self.DU_params = {
            "rendah": [0, 0, 2, 6],
            "sedang": [5, 6, 10, 14],
            "tinggi": [10, 14, 24, 24]
        }

        # Output MFs Parameters
        self.Flood_params = {
            "Aman": [0, 0, 15, 40],
            "Waspada": [30, 45, 55, 70],
            "Bahaya": [60, 80, 100, 100]
        }

        self.Depth_params = {
            "Rendah": [0, 0, 0.3, 0.9],
            "Sedang": [0.6, 1.2, 1.8, 2.2],
            "Tinggi": [1.8, 2.2, 3, 3]
        }

        # Rules (CR, WL, DU -> Flood, Depth)
        self.rules = [
            ( "rendah","rendah","rendah", "Aman","Rendah"),
            ( "rendah","rendah","sedang", "Aman","Rendah"),
            ( "rendah","rendah","tinggi", "Waspada","Sedang"),
            ( "rendah","sedang","rendah", "Waspada","Sedang"),
            ( "rendah","sedang","sedang", "Waspada","Sedang"),
            ( "rendah","sedang","tinggi", "Waspada","Sedang"),
            ( "rendah","tinggi","rendah", "Waspada","Sedang"),
            ( "rendah","tinggi","sedang", "Waspada","Sedang"),
            ( "rendah","tinggi","tinggi", "Bahaya","Tinggi"),
            ( "sedang","rendah","rendah", "Waspada","Sedang"),
            ( "sedang","rendah","sedang", "Waspada","Sedang"),
            ( "sedang","rendah","tinggi", "Waspada","Sedang"),
            ( "sedang","sedang","rendah", "Waspada","Sedang"),
            ( "sedang","sedang","sedang", "Waspada","Sedang"),
            ( "sedang","sedang","tinggi", "Bahaya","Tinggi"),
            ( "sedang","tinggi","rendah", "Bahaya","Tinggi"),
            ( "sedang","tinggi","sedang", "Bahaya","Tinggi"),
            ( "sedang","tinggi","tinggi", "Bahaya","Tinggi"),
            ( "tinggi","rendah","rendah", "Waspada","Sedang"),
            ( "tinggi","rendah","sedang", "Waspada","Sedang"),
            ( "tinggi","rendah","tinggi", "Bahaya","Tinggi"),
            ( "tinggi","sedang","rendah", "Bahaya","Tinggi"),
            ( "tinggi","sedang","sedang", "Bahaya","Tinggi"),
            ( "tinggi","sedang","tinggi", "Bahaya","Tinggi"),
            ( "tinggi","tinggi","rendah", "Bahaya","Tinggi"),
            ( "tinggi","tinggi","sedang", "Bahaya","Tinggi"),
            ( "tinggi","tinggi","tinggi", "Bahaya","Tinggi")
        ]

        # Universe arrays for plotting/defuzz
        self.x_flood = np.linspace(0, 100, 1001)
        self.x_depth = np.linspace(0, 3, 301)

        # Precompute output MFs (arrays)
        self.flood_mfs = {k: self.trapmf(self.x_flood, v) for k, v in self.Flood_params.items()}
        self.depth_mfs = {k: self.trapmf(self.x_depth, v) for k, v in self.Depth_params.items()}

    @staticmethod
    def trapmf(x: np.ndarray, params: List[float]) -> np.ndarray:
        """Fungsi keanggotaan trapesium untuk array numpy."""
        a, b, c, d = params
        y = np.zeros_like(x, dtype=float)
        
        # rising
        idx = (x >= a) & (x <= b)
        if b - a != 0:
            y[idx] = (x[idx] - a) / (b - a)
        
        # top
        idx = (x > b) & (x < c)
        y[idx] = 1.0
        
        # falling
        idx = (x >= c) & (x <= d)
        if d - c != 0:
            y[idx] = (d - x[idx]) / (d - c)
            
        return np.clip(y, 0, 1)

    @staticmethod
    def scalar_trapmf(val: float, params: List[float]) -> float:
        """Fungsi keanggotaan trapesium untuk nilai skalar."""
        a, b, c, d = params
        if val <= a:
            return 0.0 if a != b else (1.0 if val == a else 0.0)
        if a < val <= b:
            return (val - a) / (b - a) if (b - a) != 0 else 1.0
        if b < val < c:
            return 1.0
        if c <= val < d:
            return (d - val) / (d - c) if (d - c) != 0 else 1.0
        if val >= d:
            return 0.0 if c != d else (1.0 if val == d else 0.0)
        return 0.0

    def fuzzify_sample(self, cr: float, wl: float, du: float) -> Tuple[Dict, Dict, Dict]:
        """Menghitung derajat keanggotaan untuk input."""
        mu_cr = {k: self.scalar_trapmf(cr, p) for k, p in self.CR_params.items()}
        mu_wl = {k: self.scalar_trapmf(wl, p) for k, p in self.WL_params.items()}
        mu_du = {k: self.scalar_trapmf(du, p) for k, p in self.DU_params.items()}
        return mu_cr, mu_wl, mu_du

    def evaluate_rules(self, mu_cr: Dict, mu_wl: Dict, mu_du: Dict) -> List[Dict]:
        """Mengevaluasi rule base berdasarkan derajat keanggotaan input."""
        active = []
        for i, r in enumerate(self.rules, start=1):
            cr_l, wl_l, du_l, flood_c, depth_c = r
            # Menggunakan operator AND (min)
            firing = min(mu_cr[cr_l], mu_wl[wl_l], mu_du[du_l])
            if firing > 0:
                active.append({
                    "id": i, 
                    "antecedent": (cr_l, wl_l, du_l),
                    "firing": firing, 
                    "flood": flood_c, 
                    "depth": depth_c
                })
        return active

    def aggregate_and_defuzz(self, active_rules: List[Dict]) -> Dict[str, Any]:
        """Agregasi output dan defuzzifikasi (Centroid)."""
        agg_flood = np.zeros_like(self.x_flood)
        agg_depth = np.zeros_like(self.x_depth)
        
        for ar in active_rules:
            f_label = ar["flood"]
            d_label = ar["depth"]
            firing = ar["firing"]
            
            # Komposisi rule (clipping/min) dan Agregasi (max)
            agg_flood = np.maximum(agg_flood, np.minimum(self.flood_mfs[f_label], firing))
            agg_depth = np.maximum(agg_depth, np.minimum(self.depth_mfs[d_label], firing))
            
        # Defuzzifikasi Centroid
        flood_val = None
        depth_val = None
        
        if agg_flood.sum() > 0:
            flood_val = float((self.x_flood * agg_flood).sum() / agg_flood.sum())
        
        if agg_depth.sum() > 0:
            depth_val = float((self.x_depth * agg_depth).sum() / agg_depth.sum())
            
        return {
            "agg_flood": agg_flood, 
            "agg_depth": agg_depth,
            "flood_val": flood_val, 
            "depth_val": depth_val
        }
