import numpy as np

class MissionRelay:
    """
    Derin uzay görevleri için çok sıçramalı (multi-hop) haberleşme ve rota optimizasyonu.
    Dijkstra algoritması ile en yüksek SNR yolunu bulur.
    """
    def __init__(self, engine):
        self.engine = engine
        # Düğüm Tanımları (AU cinsinden pozisyonlar)
        self.nodes = {
            "Dünya": {"type": "Yer İstasyonu", "pos": 0},
            "Lunar-Gateway": {"type": "Orbiter", "pos": 0.00257},
            "Mars-Relay": {"type": "Orbiter", "pos": 1.52},
            "Deep-Space-Probe": {"type": "Sonda", "pos": 5.2}
        }

    def calculate_hop_snr(self, node_a, node_b):
        """İki düğüm arasındaki tahmini SNR'ı hesaplar."""
        dist = abs(self.nodes[node_a]["pos"] - self.nodes[node_b]["pos"])
        if dist == 0: return 100
        # Basit bütçe modeli: 80 - 20*log10(d)
        snr = 80 - (20 * np.log10(dist * 1.5e8 + 1))
        return max(5, snr)

    def optimize_path(self, start_node, end_node):
        """Dijkstra ile en yüksek toplam SNR sağlayan yolu bulur."""
        import heapq
        
        # En kısa yol algoritmasını SNR maksimizasyonu için uyarlıyoruz
        queue = [(0, start_node, [])]
        visited = set()
        
        while queue:
            (cost, current, path) = heapq.heappop(queue)
            
            if current in visited: continue
            visited.add(current)
            
            path = path + [current]
            
            if current == end_node:
                return path, -cost
            
            for neighbor in self.nodes:
                if neighbor not in visited:
                    hop_snr = self.calculate_hop_snr(current, neighbor)
                    # Kümülatif maliyet (negatif SNR)
                    heapq.heappush(queue, (cost - hop_snr, neighbor, path))
        
        return [start_node, end_node], 0
