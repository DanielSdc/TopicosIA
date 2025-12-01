package com.topai.incidenciasestacionamiento.dto.response;

import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class UsuarioResponseDTO {
    private Long id;
    private String correo;
    private String nombre;
    private String role;
    private PropietarioResponseDTO propietario;
}
