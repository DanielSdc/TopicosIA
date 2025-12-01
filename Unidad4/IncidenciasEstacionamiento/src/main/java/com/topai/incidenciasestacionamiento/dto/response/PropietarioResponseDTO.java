package com.topai.incidenciasestacionamiento.dto.response;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class PropietarioResponseDTO {
    private Long id;
    private String nombre;
    private String direccion;
    private String correoUsuario;
    private boolean tarjetaPase;
}
