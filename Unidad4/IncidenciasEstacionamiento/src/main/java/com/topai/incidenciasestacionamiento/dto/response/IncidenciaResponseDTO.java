package com.topai.incidenciasestacionamiento.dto.response;

import lombok.Builder;
import lombok.Data;

import java.time.LocalDateTime;

@Data
@Builder
public class IncidenciaResponseDTO {
    private Long id;
    private LocalDateTime fecha;
    private Double longitud;
    private Double latitud;
    private AutomovilResponseDTO automovil;
    private UsuarioResponseDTO usuario;
}
