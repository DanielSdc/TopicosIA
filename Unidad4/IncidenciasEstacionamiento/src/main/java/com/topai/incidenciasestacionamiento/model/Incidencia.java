package com.topai.incidenciasestacionamiento.model;

import jakarta.persistence.*;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

import java.time.LocalDateTime;

@Entity
@Data
@Builder
@NoArgsConstructor
@AllArgsConstructor
@Table (name = "incidencias")
public class Incidencia {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    private LocalDateTime fecha;
    private Double longitud;
    private Double latitud;

    @ManyToOne
    @JoinColumn(name = "automovil_id")
    private Automovil automovil;

    @ManyToOne
    @JoinColumn(name = "usuario_id")
    private Usuario usuario;
}
