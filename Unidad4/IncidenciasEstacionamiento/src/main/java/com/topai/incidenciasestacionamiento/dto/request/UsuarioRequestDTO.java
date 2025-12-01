package com.topai.incidenciasestacionamiento.dto.request;

import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class UsuarioRequestDTO {
    @Email
    private String correo;
    @NotBlank
    private String nombre;
}
